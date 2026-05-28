---
name: dependency-audit
description: "Audit Ruby on Rails dependencies, gems, JavaScript packages, containers, CI, and supply-chain controls for known vulnerabilities and risky upgrade paths. Use when the user mentions dependency audit, bundle audit, brakeman, Rails CVE, Ruby gem vulnerability, npm audit, CVE, vulnerable gems, outdated Rails, supply chain security, or Rails upgrade risk."
allowed-tools: Bash, Read, Grep, Glob, WebSearch
---

# Dependency Audit — Rails Stack and Supply Chain Security

Audit the Rails application's runtime stack, gems, JavaScript packages, deployment images, CI, and supply-chain controls. Treat tool output as evidence to verify, not proof by itself.

## Validation Runner Mode

Run this skill as validation, not education. Resolve scope, inspect manifests/tooling, and report only applicable vulnerabilities, material unknowns, and process gaps. Include package versions, lockfile evidence, tool output, exposure classification, and fix/version guidance. Do not dump raw scanner output without triage.

## Authorization Check

Only audit projects the user owns, maintains, or is authorized to assess. Provide remediation and upgrade guidance. Do not help weaponize CVEs against unauthorized systems.

## Step 1: Inventory the Rails Stack

Find manifests, lockfiles, runtime files, and deployment descriptors:

```text
Ruby/Rails: Gemfile, Gemfile.lock, .ruby-version, .ruby-gemset, config/application.rb
Rails config: config/environments/*.rb, config/initializers/*.rb, config/storage.yml, config/cable.yml
JavaScript: package.json, package-lock.json, yarn.lock, pnpm-lock.yaml, bun.lockb
Containers: Dockerfile, docker-compose.yml, .dockerignore
CI/CD: config/ci.rb, .github/workflows, .gitlab-ci.yml, CircleCI, Buildkite, Jenkinsfile
Deploy: Procfile, app.json, render.yaml, fly.toml, railway.json, heroku.yml, kamal config
Infrastructure: Terraform, CloudFormation, Pulumi, Helm, Kubernetes manifests
```

Run local inventory commands when the repo allows it:

```bash
ruby -v
bundle -v
bundle exec rails -v 2>/dev/null || bin/rails -v
bundle list 2>/dev/null | head -100
bundle exec rails middleware 2>/dev/null
bundle exec rails routes 2>/dev/null | head -100
```

Catalog these components:

- Rails, Ruby, Bundler, Rack, Puma/Passenger, database adapter, Redis client, ActiveStorage service, ActionCable adapter.
- Auth: Devise, OmniAuth, Rodauth, Clearance, Sorcery, Authlogic.
- Authorization: Pundit, CanCanCan.
- Admin and operations engines: Sidekiq::Web, PgHero, Mission Control Jobs, Flipper UI, GoodJob, Blazer, RailsAdmin, ActiveAdmin, Avo, Administrate, LetterOpenerWeb.
- Security controls: rack-attack, brakeman, bundler-audit, importmap audit, Rails local CI, doorkeeper, rack-cors, secure_headers, lockbox, attr_encrypted, Active Record Encryption.
- Providers: Stripe, Braintree, PayPal, SendGrid, Resend, Postmark, Twilio, AWS/GCP/Azure SDKs.
- Frontend: import maps, sprockets, webpacker, jsbundling-rails, vite, Turbo, Stimulus, React/Vue packages.

## Step 2: Run Audit Tools

Run what applies. If a tool is missing, report that gap and suggest adding it.

```bash
# Ruby and Rails
bundle audit check --update
bundle exec brakeman -q
bundle exec brakeman -q -f json
bundle outdated --strict
bundle exec rubocop --only Security 2>/dev/null || true
bundle exec bearer scan . 2>/dev/null || true
bundle exec dawn 2>/dev/null || true
bin/importmap audit 2>/dev/null || true

# JavaScript assets
npm audit --json
npm audit --omit=dev --json
yarn npm audit --recursive 2>/dev/null || yarn audit 2>/dev/null
pnpm audit --json

# Containers and filesystem
trivy fs .
trivy image <image>
docker scout cves <image>
```

Do not run forced upgrades without user approval. For `npm audit fix --force`, Rails major upgrades, Ruby upgrades, or Rack/Rails jumps, inspect the resolver plan first and verify the app boots afterward.

Triage scanner output by risk: start with critical and high findings, verify applicability, document false positives separately, then work downward. After each fix, run the relevant tests and boot checks before deployment.

## Step 3: Classify Exposure

For each advisory, decide how the vulnerable component runs:

- **Runtime:** web process, worker, ActionCable, mailer, job scheduler, console tasks used in production.
- **Build-time:** asset compilation, Docker build, CI, code generation.
- **Development/test:** local tools, test helpers, preview-only services.
- **Transitive:** reachable only through a parent gem/package. Verify the vulnerable function is used.
- **Unknown:** not enough evidence. Mark it as unknown instead of overstating risk.

For Ruby, inspect Gemfile groups and deployment behavior. For JavaScript, compare production and full audit output.

## Step 4: Verify Rails-Specific Risk

### Core Rails, Rack, and Ruby

Check exact patch levels for:

- `rails`, `actionpack`, `actionview`, `activerecord`, `activesupport`, `activestorage`, `actionmailbox`, `actioncable`.
- `rack`, `rack-session`, `rack-cors`, `puma`, `passenger`, `bootsnap`.
- Web/app server and host components: Nginx, Apache, Puma, Passenger, OpenSSH, ImageMagick/libvips/ffmpeg.
- Ruby patch level and EOL status.
- Supported Rails security window. As of April 2026, Rails 8.1.3 is the latest release, with security patches shipping for the 7.2, 8.0, and 8.1 lines.
- Legacy Rails apps before strong parameters need explicit mass-assignment protections such as `attr_accessible` allowlists or a documented upgrade plan.

Review security-sensitive configuration:

- `secret_key_base`, cookie salts, cookie digest/cipher settings, and rotation plans.
- Cookie serializer and legacy `Marshal`/YAML migration risk.
- Host authorization, `force_ssl`, secure cookies, HSTS, CSP, Permissions-Policy, CORS, and Rails default security headers.
- Parameter filtering for passwords, secrets, tokens, keys, OTP codes, certificates, and sensitive identifiers such as SSNs.
- Active Record Encryption for sensitive model attributes.
- Rails 8 `params.expect` usage where available, especially on create/update paths.
- `perform_deep_munge` disabled and whether nil-array query behavior is handled safely.
- Error pages and debug configuration per environment.
- API-only apps with browser-reachable endpoints and no CSRF/origin equivalent.

### Brakeman and bundler-audit

- Read Brakeman findings and ignored warnings.
- An ignored Brakeman warning needs a reason, owner, date, and re-evaluation trigger.
- Verify `bundle audit` findings against `Gemfile.lock`, not a loose version constraint.
- Do not treat clean tool output as a clean audit. Tools miss business logic, IDOR, tenant isolation, provider races, and exposed admin engines.

### Auth and Authorization Dependencies

Check installed versions and configuration for:

- Rails generated authentication / `has_secure_password`: bcrypt present, minimum password rules added, reset-token expiry reviewed.
- Devise: `:validatable`, password length, lockable, timeoutable, rememberable, reset-token expiry, reconfirmable, OmniAuth callbacks.
- Pundit/CanCanCan: controller coverage, policy scopes, `skip_authorization`, `skip_policy_scope`.
- OmniAuth: CSRF/state protections, redirect validation, account linking.
- Doorkeeper/OAuth: token expiry, refresh-token rotation, PKCE, public/confidential client separation, admin UI exposure.

### Mounted Engines and Dashboards

Grep `config/routes.rb` for operations surfaces:

```bash
grep -rn "Sidekiq::Web\|PgHero\|Flipper\|GoodJob\|Blazer\|RailsAdmin\|ActiveAdmin\|Avo\|Administrate\|LetterOpener" config/routes.rb config/routes 2>/dev/null
```

Verify every mounted engine has authentication in staging, review apps, and production. Avoid auth guards that silently fail open when env vars are unset.

### ActiveStorage and File Processing

Review gems and system packages used for uploads and previews:

- ImageMagick, libvips, Poppler, ffmpeg, Marcel, MiniMagick, ruby-vips.
- Public vs private buckets.
- SVG/HTML/PDF/Office handling.
- Direct upload endpoint exposure.
- Signed URL expiry.

### Background Jobs and Providers

Audit Sidekiq, ActiveJob, Redis, payment, email, and webhook dependencies:

- Idempotency keys and retry behavior.
- Atomic job claiming before side effects.
- Constant-time webhook signature verification.
- Finite timestamp parsing and replay windows.
- Provider IDs that should not be overwritten while previous resources are in flight.

## Step 5: Supply Chain Review

Check for:

- Missing or uncommitted lockfiles.
- Private gem/package names that could be claimed publicly.
- Mixed gem sources without source blocks.
- Unpinned Git gems, branch-based dependencies, or direct GitHub dependencies.
- Native extensions or install scripts in sensitive packages.
- Unmaintained gems in auth, crypto, file parsing, PDF/XML/YAML, payments, and admin surfaces.
- Image/video/archive processing dependencies such as ImageMagick, libvips, ffmpeg, Paperclip, MiniMagick, Poppler, and archive libraries with unsafe defaults or stale CVEs.
- CI actions pinned to branches instead of versions or SHAs.
- `pull_request_target` workflows that check out untrusted code with secrets.
- Rails 8.1 `config/ci.rb` missing security checks: tests, Brakeman, Bundler Audit, and `bin/importmap audit` when import maps are used.
- Vulnerable gems upgraded with a conservative plan such as `bundle update --conservative gem_name` when possible.
- Bundler trust policy or equivalent provenance controls considered for high-sensitivity deployments.
- `bin/rails credentials:fetch` in deploy scripts. Treat any environment that can fetch production credentials as part of the production trust boundary.
- Dependency and platform update process with normal cadence, security triage cadence, and emergency patch path. Dependabot, GitHub/GitLab security alerts, OS package alerts, provider security notices, and client/customer support obligations should feed that process.
- Clear owner, severity target, communication path, and time estimate process for urgent security updates.
- Docker `latest` tags, root containers, secrets in build args, and stale base images.

## Output Format

```markdown
# Rails Dependency and Supply Chain Audit
## Project
## Rails/Ruby Version
## Date

### Stack Inventory
| Component | Installed | Latest/Secure | Exposure | Notes |
|-----------|-----------|---------------|----------|-------|

### Known Vulnerabilities
| Package | Installed | Advisory/CVE | Severity | Exposure | Fix Version | Applicability |
|---------|-----------|--------------|----------|----------|-------------|---------------|

### Rails Configuration Risks
#### [SEVERITY] [Title]
**File:** `path:line`
**Component:** [gem/framework/tool]
**Exposure:** Runtime | Build-time | Dev-only | Test-only | Unknown
**Issue:** [specific risk]
**Evidence:** [tool output or code]
**Remediation:** [version/config change]
**Verification:** [command proving the fix]
**Disposition:** Fixed | Deferred | Accepted Risk

### Supply Chain Risks
| Risk | Component | Evidence | Remediation |
|------|-----------|----------|-------------|

### Security Tooling Coverage
| Tool | Present | Runs in CI | Notes |
|------|---------|------------|-------|
| Brakeman | | | |
| bundler-audit | | | |
| RuboCop Security cops | | | |
| Bearer or equivalent SAST/privacy scanner | | | |
| Dependabot/GitHub/GitLab security alerts | | | |
| False-positive tracking | | | |
| Post-fix regression tests | | | |

### Prioritized Action Plan
1. [Critical runtime CVEs or exposed admin surfaces]
2. [High reachable vulnerabilities]
3. [Medium upgrade/config work]
4. [Low maintenance improvements]
5. [Accepted risks with compensating controls]
```

## Boundaries

- Audit only code, lockfiles, configs, images, and dependency data the user provides or authorizes.
- Verify each advisory applies to the installed version and reachable configuration.
- Provide specific fix versions, upgrade paths, or compensating controls.
- Warn when a fix may break Rails behavior or require a migration.
- Refuse to help exploit vulnerabilities against unauthorized targets.

## References

- Rails Security Guide
- Rails security announcements
- Saeloun Rails Security Best Practices guide
- Historical Rails 2.3 Security Guide threat model
- Ruby Advisory DB and bundler-audit
- Brakeman
- OWASP Ruby on Rails Cheat Sheet
- GitHub Advisory Database
- NVD
- SLSA supply-chain guidance
