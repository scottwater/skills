---
name: rails-security-validation
description: "Coordinate validation-focused Ruby on Rails security reviews across authentication, authorization, OWASP risks, dependencies, runtime configuration, cloud/platform settings, and security operations. Use when the user wants to run the Rails security skills as a validation runner against a repo, branch, diff, pull request, or changed files and receive evidence-backed pass/fail findings instead of educational guidance."
allowed-tools: Read, Grep, Glob, Bash
---

# Rails Security Validation Runner

Run a validation-focused Rails security review. This skill is not a tutorial and not a general code review. It verifies whether a Rails application satisfies concrete security expectations and reports only evidence-backed findings, validation gaps, and recommended checks.

Use this coordinator for broad Rails security validation. If the user asks for one area only, use the relevant specialist directly:

- `rails-auth-audit`: authentication, authorization, policy coverage, roles, tenants, sessions, tokens, and controller access.
- `owasp-audit`: OWASP-style Rails appsec validation across input handling, XSS, SQL injection, CSRF, SSRF, file handling, logging, and misconfiguration.
- `dependency-audit`: Rails/Ruby/JS/container dependency, CVE, supply-chain, and security tooling validation.
- `cloud-audit`: Rails infrastructure, secrets, platform, storage, database, Redis/Memcached, CI/CD, logging, endpoint, and cloud hardening validation.

The specialist skills must remain independently runnable. This coordinator resolves scope once, gathers shared context, runs or simulates each lens, and merges the results.

## Authorization Check

Before validation, confirm the user owns, maintains, or is authorized to assess the repository, application, environment, cloud account, or diff. If the request includes live scanning, cloud CLI access, production data, or external targets, ask for explicit scope and authorization.

## Scope Resolution

First establish what to validate and report it briefly.

If the user provides an explicit range, branch, PR, commit, date range, file list, environment, or full-repo request, use that scope. If no scope is provided:

- For a git repo with changes, validate pending tracked changes against `HEAD`.
- If no pending changes exist, validate the current branch against `main...HEAD`.
- If `main` is unavailable, try `origin/main...HEAD`.
- If there is no useful diff, validate the whole repository at the current checkout.

Common scopes:

```sh
# Pending tracked changes
git status --short
git diff --name-status HEAD
git diff --stat HEAD

# Staged changes only
git diff --cached --name-status
git diff --cached --stat

# Current branch compared to main
git diff --name-status main...HEAD
git diff --stat main...HEAD
git log --oneline main..HEAD

# Whole repo inventory
find . -maxdepth 3 -type f \( -name Gemfile -o -name Gemfile.lock -o -name config.ru -o -name routes.rb -o -name '*.rb' \) | sort
```

If scope is ambiguous, ask one short clarifying question. Otherwise, choose the most likely scope, state it, and proceed.

## Validation Workflow

1. Resolve scope and authorization.
2. Identify Rails version, Ruby version, auth stack, policy framework, dependency manifests, deployment/platform files, and security tooling.
3. Inspect changed files first when validating a diff. Do not review unrelated areas unless the diff touches a shared security boundary.
4. Run the four validation lenses in parallel when the harness supports separate agents. If not, run them sequentially yourself.
5. Merge findings, deduplicate overlap, and preserve the strongest severity.
6. Report only validation failures, material unknowns, and high-value checks. Do not explain Rails security basics.

## Shared Discovery Commands

Run safe local commands when available:

```sh
ruby -v
bundle -v
bundle exec rails -v 2>/dev/null || bin/rails -v 2>/dev/null || true
bundle exec rails routes 2>/dev/null || bin/rails routes 2>/dev/null || true
bundle exec rails middleware 2>/dev/null || true
```

Inventory security-relevant files:

```sh
find app config db lib -maxdepth 4 -type f 2>/dev/null | sort
find . -maxdepth 3 -type f \( -name Gemfile -o -name Gemfile.lock -o -name package.json -o -name yarn.lock -o -name package-lock.json -o -name pnpm-lock.yaml -o -name Dockerfile -o -name 'docker-compose*.yml' -o -name '*.tf' -o -name '*.yml' -o -name '*.yaml' \) | sort
```

Focused greps:

```sh
# Auth/authz and policy coverage
rg -n "authenticate_|current_user|current_account|authorize\b|authorize!|policy_scope|authorized_scope|skip_authorization|skip_policy_scope|Pundit|ActionPolicy|CanCan|Ability|admin\?|role|permission" app config spec 2>/dev/null

# Rails appsec sinks
rg -n "raw\(|html_safe|<%==|!= |render inline|render params|redirect_to params|Arel\.sql|find_by_sql|where\(\"|order\(params|pluck\(params|sum\(params|eval\(|system\(|Open3|Kernel\.open|IO\.popen|send_file|send_data|URI\.open|Net::HTTP|Faraday|HTTParty|RestClient" app lib config 2>/dev/null

# Rails security defaults and configuration
rg -n "protect_from_forgery|skip_before_action :verify_authenticity_token|csrf_meta_tags|force_ssl|config\.hosts|host_authorization|content_security_policy|permissions_policy|rack-cors|filter_parameters|perform_deep_munge|rate_limit|Rack::Attack" app config 2>/dev/null

# Secrets and sensitive files
rg -n "RAILS_MASTER_KEY|secret_key_base|SECRET_KEY_BASE|DATABASE_URL|REDIS_URL|api_key|private_key|password|token|credentials" --glob '!tmp/**' --glob '!log/**' . 2>/dev/null
```

Run audit tools when installed and safe:

```sh
bundle audit check --update 2>/dev/null || true
bundle exec brakeman -q 2>/dev/null || true
bundle exec rubocop --only Security 2>/dev/null || true
bin/importmap audit 2>/dev/null || true
npm audit --omit=dev --json 2>/dev/null || true
```

## Validation Lenses

### 1. Access And Authorization Validation

Use `rails-auth-audit` logic to validate:

- Protected routes require authentication.
- Controller actions, GraphQL resolvers, jobs, mailers, exports, and mounted engines enforce authorization.
- Pundit, Action Policy, CanCanCan, or custom policies cover each sensitive action.
- Policy scopes protect lists, counts, filters, search, exports, dashboards, select boxes, broadcasts, and background jobs.
- Strong params / `params.expect` do not allow privilege fields or cross-tenant foreign keys without validation.
- Sessions rotate, expire, and avoid sensitive business state.
- Reset, invitation, activation, and magic-link tokens expire, reject blank tokens, and avoid enumeration.
- Admin, billing, export, impersonation, and support workflows require strong auth and audit logging.

### 2. Rails AppSec Validation

Use `owasp-audit` logic to validate:

- SQL and reporting query sinks use binds, allowlists, and `sanitize_sql_like` where needed.
- XSS sinks avoid unsafe `raw`, `.html_safe`, `<%==`, Haml `!=`, unsafe `_html` translations, unquoted attributes, and unsafe rich text.
- CSRF protection covers browser-cookie paths, Turbo/custom JS sends tokens, and GET routes do not mutate state.
- Redirects, render paths, headers, files, uploads, downloads, and external fetches do not accept unsafe user input.
- File and media processing has type, extension, size, archive, malware, and async/rate-limit controls.
- Logs, errors, analytics, and emails do not expose sensitive values.
- Security headers, CSP, host authorization, CORS, cookies, and `force_ssl` are configured for production.

### 3. Dependency And Tooling Validation

Use `dependency-audit` logic to validate:

- Rails, Ruby, Rack, Puma/Passenger, gems, JS packages, containers, and OS-facing dependencies are supported and patched.
- Brakeman, bundler-audit, importmap audit, security RuboCop cops, and dependency alerts run in CI or an equivalent process.
- Vulnerable dependencies have an owner, severity, applicability decision, fix version, and test plan.
- New gems are necessary, maintained, licensed acceptably, pinned/constrained, and do not add risky transitive dependencies.
- Security scanner false positives are tracked separately from unresolved findings.
- The team has normal, security, and emergency patch cadences.

### 4. Runtime, Cloud, And Operations Validation

Use `cloud-audit` logic to validate:

- Production secrets, credentials, cookie keys, deployment variables, and workstation access are managed as production trust boundaries.
- Databases, Redis, Memcached, object storage, queues, dashboards, and admin panels are private or strongly authenticated.
- ActiveStorage buckets and direct uploads enforce access, CORS, signed URL expiry, and public/private separation.
- CI/CD protects secrets, pins actions/images, and avoids untrusted PR execution with credentials.
- Logs, alerts, endpoint monitoring, WAF/CDN/rate limits, and incident response hooks exist for security-relevant events.
- OS, SSH, web servers, app servers, and media tooling are patched and hardened.

## Evidence Rules

Each finding must include evidence from at least one of:

- File path and line number.
- Route output or middleware output.
- Tool output.
- Config value.
- Test/spec gap tied to a route, role, policy, or controller.
- Explicit unknown caused by missing files, unavailable tooling, or no environment access.

Mark findings as:

- **Fail:** Evidence shows the control is missing or unsafe.
- **Unknown:** The control might exist, but the repository or available environment does not prove it.
- **Pass:** Only include pass items when the user asks for a checklist or attestation.

## Output Format

```md
# Rails Security Validation Report

Scope: `<range or repository>`
Rails/Ruby: `<versions if detected>`
Validation date: `<date>`

## Executive Summary
- Critical: X | High: X | Medium: X | Low: X | Unknown: X
- Highest-risk gaps: [short list]

## Findings

### High: Cross-Tenant Project Access Is Not Policy Scoped
Status: Fail
Lens: Access And Authorization
Evidence: `app/controllers/projects_controller.rb:42`, `app/policies/project_policy.rb:18`

The controller loads `Project.find(params[:id])` before authorization. A user may be able to address another tenant's project by ID before the policy runs.

Required validation:
- Request spec for owner, member, cross-tenant user, and anonymous user.
- Verify lists, counts, exports, and autocomplete use the same policy scope.

Recommended fix:
- Load through `current_account.projects.find(params[:id])` or `policy_scope(Project).find(params[:id])`.

## Unknowns
- [Control that could not be validated and why]

## Suggested Validation Commands
- [commands/specs to run next]
```

Severity guide:

- **Critical:** confirmed auth bypass, cross-tenant exposure, exposed production secrets, public admin/dashboard, reachable RCE, unsafe file execution, actively exploitable dependency with runtime exposure.
- **High:** likely authz gap, missing policy scope on sensitive data, dangerous XSS/SQL/SSRF/file sink, CSRF on state-changing cookie-auth path, unsupported Rails/Ruby with known security exposure.
- **Medium:** missing lower-permission tests, scanner/tooling gaps, weak headers/CSP/CORS, rate-limit gaps, unsafe upload processing, logging/PII risks.
- **Low:** hardening gaps, documentation/process gaps, low-risk outdated packages, optional defense-in-depth.
- **Unknown:** material control not provable from available evidence.

## What Not To Do

- Do not teach Rails security concepts unless the user asks.
- Do not list every checklist item.
- Do not report speculative issues as confirmed findings.
- Do not count a scanner warning as a vulnerability until applicability is checked.
- Do not count `authenticate_user!` as authorization.
- Do not count view-level hidden buttons as access control.
- Do not accept admin-only happy-path specs as coverage for permission-sensitive behavior.
- Do not ignore unknowns when they block validation.
