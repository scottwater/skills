---
name: osint-recon
description: "Gather public open source intelligence for authorized Ruby on Rails application security research, attack surface assessment, threat intelligence, and pre-audit scoping. Use when the user mentions OSINT, public footprint, Rails target research, exposed repos, leaked credentials, technology discovery, domain investigation, company recon, or threat intel for a Rails app."
allowed-tools: Bash, WebSearch, WebFetch, Read
---

# OSINT Recon — Rails Application Intelligence

Gather and correlate public information that helps assess a Ruby on Rails application's security posture. Focus on stack clues, exposed environments, public code, leaked secrets, operational surfaces, and breach context.

## Validation Runner Mode

Run this skill as validation, not education. Resolve the public-source scope, collect source-attributed evidence, and report only security-relevant public findings, material unknowns, confidence, and next authorized checks. Do not provide doxing or personal profiling.

## Ethics Check

Before proceeding, confirm:

1. The investigation has a legitimate purpose: defensive research, authorized assessment, bug bounty, threat intelligence, or CTF.
2. You will use public sources only.
3. Results will not support harassment, stalking, doxing, or unauthorized access.

Refuse requests that target individuals for harassment or aggregate personal data beyond the stated security objective.

## Collection Plan

### Domain and Infrastructure OSINT

```bash
whois <domain>
dig A <domain>
dig AAAA <domain>
dig MX <domain>
dig TXT <domain>
dig NS <domain>
```

Certificate transparency:

```bash
curl -s "https://crt.sh/?q=%25.<domain>&output=json" | jq -r '.[].name_value' | sort -u
```

Look for Rails deployment patterns:

- Heroku, Render, Fly.io, Hatchbox, Kamal, Kubernetes ingress, Nginx, Puma, Passenger.
- Subdomains: `app`, `api`, `admin`, `staging`, `review`, `demo`, `sidekiq`, `jobs`, `status`, `assets`, `cdn`.
- Storage/CDN: S3, CloudFront, GCS, Azure Blob, Fastly, Cloudflare.
- Email and auth providers: SendGrid, Postmark, Resend, Mailgun, Auth0, Okta, Google Workspace.

### Public Code and Configuration

Search public repositories, gists, issue trackers, package registries, docs, and support forums for:

- `Gemfile`, `Gemfile.lock`, `.ruby-version`, `config/routes.rb`.
- Rails credentials mistakes: `config/master.key`, `RAILS_MASTER_KEY`, `secret_key_base`, `.env`.
- Provider keys and Rails env vars: `DATABASE_URL`, `REDIS_URL`, `STRIPE_SECRET_KEY`, `AWS_ACCESS_KEY_ID`, `S3_BUCKET`, `SENDGRID_API_KEY`.
- Internal routes, admin mounts, webhook endpoints, Sidekiq/PgHero/Flipper/GoodJob/Blazer paths.
- Stack traces, logs, database dumps, seed files, fixtures, screenshots, or API examples.

Example searches:

```text
site:github.com <org> Gemfile.lock Rails
site:github.com <domain> RAILS_MASTER_KEY OR secret_key_base OR DATABASE_URL
site:<domain> filetype:env OR filetype:log OR filetype:sql
site:<domain> "Sidekiq" OR "PgHero" OR "Flipper"
```

### Search and Historical Data

Use search engines, Wayback Machine, Common Crawl, and public caches to find:

- Removed endpoints and old admin paths.
- Deprecated API versions.
- Public beta/staging/review apps.
- Old JavaScript bundles that reveal routes, feature flags, or API endpoints.
- Old docs that mention provider names, webhook paths, or tenant IDs.

### Job Postings and Organization Signals

Job postings and engineering blogs can reveal:

- Rails/Ruby versions or major upgrade blockers.
- Gems and platforms: Devise, Pundit, Sidekiq, Redis, Postgres, GraphQL, Hotwire, Stripe, S3.
- Cloud and CI: AWS, Heroku, Render, Fly, GitHub Actions, Buildkite, Terraform, Kubernetes.
- Security controls: SSO, SOC 2, audit logs, WAF, bug bounty, secrets management.

Use this to guide defensive review. Do not infer vulnerabilities from tech names alone.

### Public Documents and Metadata

For public documents:

```bash
exiftool <file>
```

Look for author names only when needed for the security objective. Prefer organizational patterns over personal profiling. Record software versions, paths, timestamps, and internal hostnames when relevant.

### Breach and Threat Intelligence

Use authorized lookups and public feeds to check:

- Known leaked domains or credential exposure. Do not distribute breach data.
- Advisories for observed Rails, Ruby, Rack, or gem versions.
- Mentions in abuse feeds, phishing kits, malware infrastructure, and paste sites.
- Typosquatted domains or lookalike login pages.

## Analysis

Correlate findings into security-relevant leads:

- Exposed non-production environments.
- Public code that reveals routes, gems, or secrets.
- Admin/ops surfaces that deserve scoped testing.
- Dependency versions that deserve verification.
- Storage buckets or CDN origins that may relate to ActiveStorage.
- Email/domain configuration that affects account takeover, phishing, or spoofing risk.
- Public docs that reveal tenant IDs, account IDs, object IDs, or API behavior.

Rate confidence:

- **High:** multiple current sources or direct evidence.
- **Medium:** one reliable source.
- **Low:** stale, inferred, or unverified.

## Output Format

```markdown
# Rails OSINT Report
## Objective
## Target
## Date

### Public Footprint
| Asset | Source | Evidence | Confidence |
|-------|--------|----------|------------|

### Rails and Stack Signals
| Signal | Evidence | Security Relevance | Confidence |
|--------|----------|--------------------|------------|

### Exposed Code, Secrets, or Config
| Finding | Source | Sensitivity | Recommended Action |
|---------|--------|-------------|--------------------|

### Potential Attack Surface Leads
| Lead | Evidence | Why It Matters | Next Authorized Check |
|------|----------|----------------|-----------------------|

### Intelligence Gaps
- [What could not be verified]

### Recommendations
1. [Defensive next step]
2. [Next]
```

## Boundaries

- Use public sources only.
- Do not access private systems, authenticated resources, leaked accounts, or stolen data.
- Do not aggregate PII beyond the security objective.
- Attribute findings to sources.
- State confidence and staleness.
- If a finding could cause harm if misused, mark it sensitive and recommend responsible handling.
- Refuse doxing, stalking, credential use, or unauthorized surveillance.

## References

- OSINT Framework
- Bellingcat Online Investigation Toolkit
- SANS OSINT resources
- Rails Security Guide
- OWASP Web Security Testing Guide
