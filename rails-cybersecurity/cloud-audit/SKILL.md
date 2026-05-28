---
name: cloud-audit
description: "Audit cloud and platform configuration for Ruby on Rails applications, including AWS, GCP, Azure, Heroku, Render, Fly.io, object storage, databases, Redis, CI/CD, secrets, IAM, and deployment hardening. Use when the user mentions Rails cloud security, AWS Rails app, Heroku audit, S3 ActiveStorage, IAM audit, cloud misconfiguration, production hardening, or platform security."
allowed-tools: Bash, Read, Grep, Glob, WebSearch
---

# Cloud Audit — Rails Infrastructure Security Review

Audit the infrastructure that runs a Ruby on Rails application: platform, IAM, database, Redis, object storage, secrets, CI/CD, networking, logging, and operational dashboards.

## Validation Runner Mode

Run this skill as validation, not education. Resolve authorized environments, inspect repository/IaC/platform evidence, and report confirmed misconfigurations, material unknowns, and concrete verification commands. Include resource names, config paths, CLI output, or unavailable-access notes for each finding.

## Authorization Check

Confirm the user owns or is authorized to review the cloud accounts, projects, apps, buckets, clusters, and environments. Do not access accounts, tenants, or data outside scope.

## Scope the Audit

Identify:

1. Hosting platform: AWS, GCP, Azure, Heroku, Render, Fly.io, Kubernetes, VPS, Hatchbox, Kamal.
2. Environments: production, staging, review apps, demos, workers, job runners.
3. Data stores: Postgres/MySQL, Redis, Elasticsearch/OpenSearch, object storage, cache, queues.
4. Rails services: web, workers, scheduler, ActionCable, ActiveStorage, cache/Memcached, mailers, webhooks.
5. Access method: cloud CLI, platform CLI, IaC files, screenshots, exported configs, read-only credentials.

## Rails Infrastructure Inventory

From the repository, review:

```text
config/database.yml
config/storage.yml
config/cable.yml
config/environments/*.rb
config/initializers/*.rb
config/ci.rb
Procfile
Dockerfile
docker-compose.yml
.github/workflows/
render.yaml
fly.toml
app.json
heroku.yml
config/deploy.yml
config/kamal/
terraform/
helm/
k8s/
```

Run safe local checks when available:

```bash
grep -RIn "DATABASE_URL\|REDIS_URL\|S3\|AWS_\|GCS\|AZURE\|RAILS_MASTER_KEY\|SECRET_KEY_BASE\|force_ssl\|active_storage\|action_cable\|credentials:fetch" config/ .github/ Dockerfile* Procfile* 2>/dev/null
```

## Audit Categories

### Identity and Access Management

Check least privilege for:

- Deploy users and CI service accounts.
- Rails runtime role or dyno credentials.
- Object storage access for ActiveStorage.
- Database and Redis users.
- Provider SDK keys: Stripe, email, SMS, OAuth, error tracking.
- Admin consoles and platform accounts.

AWS examples:

```bash
aws iam get-account-summary
aws iam list-users
aws iam generate-credential-report && aws iam get-credential-report --output text --query Content | base64 -d
```

GCP examples:

```bash
gcloud projects get-iam-policy <project-id>
gcloud iam service-accounts list
```

Azure examples:

```bash
az role assignment list --all
az ad user list
```

Review IaC for:

```text
"Action": "*"
"Resource": "*"
Principal: "*"
AdministratorAccess
Owner
Editor
Contributor
```

Flag long-lived access keys, broad storage permissions, CI secrets available to untrusted pull requests, and credentials shared across environments.

### Secrets and Rails Credentials

Check how the app receives secrets:

- `RAILS_MASTER_KEY`, `SECRET_KEY_BASE`, `DATABASE_URL`, `REDIS_URL`, cookie salts, and cookie signing/encryption settings.
- Provider secrets and webhook signing secrets.
- Platform config vars and secret managers.
- Kubernetes secrets and sealed/encrypted variants.
- CI/CD variables.

Risks:

- Secrets committed in repo, Docker layers, build args, logs, screenshots, or crash dumps.
- Same secrets reused across production and staging.
- Review apps with production secrets.
- No rotation plan after staff changes or incidents.
- `secret_key_base` rotation not paired with session invalidation, signed/encrypted cookie rotation, ActiveStorage impact review, and user re-login strategy.
- Deploy scripts that run `bin/rails credentials:fetch`. Treat any host or CI runner that can fetch production credentials as part of the production trust boundary.

### Network and Edge Controls

Check:

- TLS termination, HSTS, HTTP-to-HTTPS redirects.
- Rails `config.force_ssl`, secure cookies, trusted proxies, host authorization, CSP, Permissions-Policy, and CORS.
- `force_ssl` enabled only when production traffic reaches Rails over a correct TLS/proxy setup, so secure cookies and redirects work without lockouts.
- CDN/WAF rules for admin routes, login, password reset, uploads, APIs, and webhooks.
- Security groups/firewall rules for SSH, RDP, Postgres, Redis, Memcached, Elasticsearch, admin panels.
- SSH hardened with key-only access where applicable, no password authentication, no unnecessary public admin ports, and brute-force protection such as fail2ban or cloud firewall automation.
- Private network placement for database and Redis.
- Egress controls for SSRF-prone features.
- Rate limiting at CDN/WAF and in Rails middleware.
- DDoS and resource-exhaustion protections at CDN/load balancer/provider level for expensive Rails endpoints.

Rails-specific edge concerns:

- `X-Forwarded-For` trust with proxies.
- Host header handling, `config.hosts`, and narrow `host_authorization` exceptions.
- ActionCable origins.
- CORS for APIs and ActiveStorage direct uploads.
- Large body limits for uploads/imports.

### Database, Redis, and Queues

Check:

- Public exposure of Postgres/MySQL/Redis/Memcached.
- Memcached bound to private interfaces only, firewalled from the internet, and UDP disabled where applicable.
- TLS in transit and certificate verification.
- Encryption at rest and backup encryption.
- Backup retention and restore testing.
- Database users with least privilege.
- Redis auth, TLS, eviction policy, and persistence settings.
- Sidekiq/GoodJob dashboard exposure.
- Job queues that process untrusted uploads, webhooks, or AI/tool calls.

For managed services, verify the deployed TLS chain before changing client verification settings.

### ActiveStorage and Object Storage

For S3/GCS/Azure Blob:

- Public access blocks or equivalent.
- Bucket/container policies and ACLs.
- Server-side encryption.
- Versioning and lifecycle rules.
- Access logs.
- CORS for direct uploads.
- Signed URL expiry.
- Separation between public assets and private uploads.
- Whether user uploads are served from the app origin or isolated asset origin.

AWS S3 examples:

```bash
aws s3api list-buckets
aws s3api get-public-access-block --bucket <bucket>
aws s3api get-bucket-policy --bucket <bucket>
aws s3api get-bucket-encryption --bucket <bucket>
aws s3api get-bucket-versioning --bucket <bucket>
```

### Containers, Hosts, and Runtime

Check:

- Non-root containers.
- Minimal base images and current OS packages.
- OS and internet-facing services such as Nginx, Apache, Puma, Passenger, OpenSSH, and image/video tooling receive security patches.
- Unneeded services are disabled or unreachable.
- No secrets in image layers.
- Web, worker, database, and file-processing processes run as least-privileged OS/container users.
- Read-only filesystems where practical.
- Health checks that do not expose secrets.
- Rails logs going to centralized logging.
- Web server and app server banners do not expose unnecessary version details.
- `RAILS_ENV=production` for production.
- Asset precompile secrets not leaking into images.
- Web server document root does not expose user uploads, temporary files, backups, generated exports, `db/development.sqlite3`, `db/seeds.rb`, or configuration files.
- Kamal/Capistrano shared directories and SSH key handling.

### Platform-Specific Checks

#### Heroku

- Config vars and pipeline promotion rules.
- Review apps: inherited config vars, public URLs, weak auth, production data.
- Add-ons: Postgres, Redis, Papertrail, Sentry, scheduler.
- Dyno formation: web, worker, release phase.
- Log drains and retention.
- Heroku Postgres backups and follower access.
- Redis TLS verification caveats by plan.

#### Render / Fly.io / Railway

- Environment variable scoping.
- Preview environment secrets.
- Private networking for databases and Redis.
- Public services and internal-only services.
- Deploy hooks and build logs.
- Persistent disks and backup policy.

#### Kubernetes

- Ingress auth and TLS.
- Secrets management.
- Pod security context and root containers.
- Network policies.
- RBAC for deploy service accounts.
- Public dashboards and metrics.
- Jobs/cronjobs running Rails tasks.

### Logging, Monitoring, and Detection

Verify:

- Centralized Rails, web server, worker, database, endpoint, and cloud logs.
- Retention long enough for investigations.
- Alerts for admin login, IAM changes, secret access, bucket policy changes, database snapshots, WAF blocks, Sidekiq failures, webhook signature failures, large exports.
- CloudTrail/Audit Logs/Activity Logs across regions.
- GuardDuty/Security Command Center/Defender or equivalent.
- Host or endpoint monitoring such as OSSEC/Wazuh, EDR, antivirus/malware scanning where appropriate, and alerts for suspicious host activity.
- Object storage access logs for sensitive buckets.

### CI/CD and Supply Chain

Review:

- Unpinned GitHub Actions or mutable Docker images.
- `pull_request_target` with untrusted checkout.
- Secrets exposed to forks or preview apps.
- Rails 8.1 `config/ci.rb` exists, when used, and runs tests, Brakeman, Bundler Audit, and `bin/importmap audit` for importmap apps.
- Deploy keys with write access.
- Branch protection and required reviews.
- Build logs containing secrets.
- Security-related RuboCop rules, Brakeman, dependency audits, and optional WAF controls run before deploy.
- `bundle install` and package installs using lockfiles.
- Direct deploy from developer machines.
- Developer workstations that handle production access use full-disk encryption, MFA, password managers, endpoint protection, and secure one-time secret sharing instead of email/chat for credentials.

## Output Format

```markdown
# Rails Cloud Security Audit Report
## Application
## Provider/Platform
## Environments
## Date

### Environment Inventory
| Environment | Platform | Data Stores | Public URL | Notes |
|-------------|----------|-------------|------------|-------|

### Findings
#### [SEVERITY] [Category]: [Title]
**Resource:** [ARN/project/resource/app/bucket]
**Environment:** [production/staging/review]
**Issue:** [specific misconfiguration]
**Risk:** [impact to Rails app/data]
**Evidence:** [CLI output, config, IaC snippet]
**Remediation:** [specific change]
**Verification:** [command or runtime check]
**Availability Risk:** [possible impact]
**Disposition:** Fixed | Deferred | Accepted Risk

### Rails Platform Controls
| Control | Status | Evidence | Gap |
|---------|--------|----------|-----|

### Prioritized Action Plan
1. [Critical: exposed data/admin/secrets]
2. [High: runtime compromise paths]
3. [Medium: hardening and monitoring]
4. [Low: maintenance]
5. [Accepted risks with compensating controls]
```

## Boundaries

- Audit only authorized accounts, projects, apps, and environments.
- Do not retrieve customer data unless the user explicitly authorizes it and the audit requires it.
- Provide remediation for each finding.
- Note availability risk before tightening network, IAM, bucket, or database controls.
- Flag evidence of active compromise immediately.
- Refuse requests to exploit misconfigurations on unauthorized infrastructure.

## References

- Rails Security Guide
- OWASP Ruby on Rails Cheat Sheet
- Saeloun Rails Security Best Practices guide
- CIS Benchmarks for AWS, GCP, Azure, Kubernetes
- AWS Well-Architected Security Pillar
- Heroku, Render, Fly.io security documentation
- OWASP Cloud-Native Application Security
