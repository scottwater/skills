---
name: owasp-audit
description: "Audit Ruby on Rails application source code against OWASP Top 10 risks. Use when the user mentions OWASP, Rails security review, Ruby on Rails audit, secure code review, vulnerability audit, IDOR, XSS, SQL injection, CSRF, SSRF, auth bugs, multi-tenant authorization, or wants a Rails codebase checked for security weaknesses."
allowed-tools: Read, Grep, Glob, Bash
---

# OWASP Audit — Rails Source Code Security Review

Review a Ruby on Rails application the way a security researcher would: map routes and data flows, identify trust boundaries, inspect framework-specific sinks, verify fixes at runtime, and report evidence.

## Validation Runner Mode

Run this skill as validation, not education. Resolve scope, inspect evidence, and report only confirmed failures, material unknowns, and concrete validation gaps. Include file paths, commands, routes, tool output, or missing-test evidence for each finding. Do not explain Rails security basics unless the user asks.

## Authorization Check

Confirm the user owns, maintains, or is authorized to review the code. If authorization or scope is unclear, ask. Provide remediation, tests, and verification. Do not provide exploit playbooks for unauthorized targets.

## Scope the Audit

1. Identify Rails, Ruby, Rack, database, Redis, job processor, authentication, authorization, and deployment targets.
2. Map entry points: routes, controllers, API endpoints, GraphQL, ActionCable, jobs, mailers, webhooks, ActiveStorage, admin engines, and mounted apps.
3. Trace data flows: `params` → strong params → models/services/jobs → database/provider/filesystem → views, JSON, emails, logs, webhooks.
4. Identify identities and tenants: `current_user`, `current_account`, `current_team`, API tokens, service accounts, admin impersonation.
5. For every finding, sweep sibling paths that touch the same model, field, state transition, external resource, or rendering sink.

## Rails First-Pass Commands

Run these early, then read the flagged files.

```bash
# Framework and routes
ruby -v
bundle exec rails -v 2>/dev/null || bin/rails -v
bundle exec rails routes 2>/dev/null || bin/rails routes

# Mounted engines and admin surfaces
grep -rn "mount .*::\|Sidekiq::Web\|PgHero\|Flipper\|GoodJob\|Blazer\|RailsAdmin\|ActiveAdmin\|Avo\|Administrate\|LetterOpener" config/routes.rb config/routes 2>/dev/null

# Auth and authorization coverage
grep -rn "before_action\|skip_before_action\|authenticate_\|authorize \|policy_scope\|skip_authorization\|skip_policy_scope\|current_user\|current_account\|admin?" app/

# IDOR and tenant-boundary candidates
grep -rn "\.find(params\|find_by(id: params\|params\[:.*_id\]\|permit(.*_id\|friendly\.find(params" app/

# Injection and rendering sinks
grep -rn "raw(\|\.html_safe\|<%==\|!= \|sanitize(\|simple_format\|json_escape\|render inline\|render params\|render .*params\|Arel.sql\|find_by_sql\|where(\"\|order(params\|reorder(params\|pluck(params\|sum(params\|calculate(params\|group(params\|having(params\|delete_all\|update_all" app/

# Command, file, network, header, and SSRF sinks
grep -rn "eval(\|system(\|syscall(\|exec(\|spawn(\|Process\.exec\|Process\.spawn\|IO\.popen\|IO\.read\|IO\.readlines\|IO\.foreach\|IO\.binread\|IO\.binwrite\|IO\.write\|Open3\|%x\[\|`.*`\|Kernel.open\|open(\"|open('|File\.open\|File\.read\|File\.write\|send_file\|send_data\|response\.headers\|headers\[\|URI.open\|OpenURI\|Net::HTTP\|Faraday\|HTTParty\|RestClient" app/ lib/ config/

# Secrets, TLS, and config risks
grep -rn "VERIFY_NONE\|verify_mode\|secret_key_base\|RAILS_MASTER_KEY\|password\|api_key\|private_key\|credentials" --include="*.rb" --include="*.yml" --include="*.yaml" --include="*.json" --include="*.env*" .

# Rails security defaults and newer security helpers
grep -rn "params.expect\|filter_parameters\|rate_limit\|force_ssl\|default_headers\|content_security_policy\|permissions_policy\|csrf_meta_tags\|default_protect_from_forgery\|perform_deep_munge\|host_authorization\|config.hosts\|authenticate_by\|has_secure_password\|encrypts " app/ config/ lib/ 2>/dev/null

# Validation regexes, routing, templates, and translations
grep -rn "validates.*format\|format:.*with:\|/\^.*\$/" app/models app/validators lib/ 2>/dev/null
grep -rn "match .*:controller\|:action\|redirect_to params\|render params\|render .*params\|_html:" config app/ 2>/dev/null
```

## OWASP Review Checklist for Rails

### A01: Broken Access Control

Check the highest-risk Rails bugs first.

- `Model.find(params[:id])` or `find_by(id: params[:id])` without tenant scoping.
- Strong params or Rails 8 `params.expect` declarations that permit foreign keys or privilege fields: `account_id`, `team_id`, `organization_id`, `project_id`, `user_id`, `role_id`, `admin`, `permission`, `plan_id`. Parameter filtering does not replace authorization.
- Controller actions, jobs, mailers, GraphQL resolvers, exports, and webhooks that modify tenant data without policy checks.
- Admin namespaces and mounted engines protected only in production or by optional env vars.
- State transitions where one route enforces ownership or immutability but sibling routes do not.
- Open redirects via `return_to`, `next`, `redirect`, `continue`, `url`, or `allow_other_host: true`.
- CSRF gaps on browser-reachable API endpoints, webhook confusion, or state-changing `GET` routes. GET must stay read-only.
- Missing `protect_from_forgery`, disabled `default_protect_from_forgery`, missing `csrf_meta_tags` for Turbo/custom JavaScript forms, or custom fetch/XHR code that omits `X-CSRF-Token`.
- Persistent cookies that survive an `ActionController::InvalidAuthenticityToken` failure. Clear remember-me or other auth cookies on CSRF failure.
- JavaScript/JSONP-style responses intended for `<script>` tags. Do not expose sensitive data through cross-site script-loadable endpoints.
- Hidden fields, disabled form controls, JavaScript-only validation, or obscured IDs treated as security controls. Treat every parameter as attacker-controlled.
- `config.action_dispatch.perform_deep_munge = false` without explicit handling of `nil` array parameters in token, ID, and lookup paths.

Prefer scoped lookups such as `current_account.projects.find(params[:id])`, policy scopes, and database constraints that enforce ownership.

### A02: Cryptographic Failures

- Hardcoded secrets in source, config, logs, sample files, CI, or deploy manifests.
- `config/master.key`, `RAILS_MASTER_KEY`, `secret_key_base`, API keys, provider secrets, private keys.
- Weak, reused, or non-random `secret_key_base`; exposed secrets without a cookie/session rotation and user re-login plan.
- Signed/encrypted cookie rotations, salts, ciphers, and digests changed without a compatibility and removal plan.
- TLS verification disabled for Redis, Postgres, HTTP clients, webhooks, or provider SDKs.
- Shared-secret comparisons using `==` instead of `ActiveSupport::SecurityUtils.secure_compare` or `fixed_length_secure_compare`.
- Sensitive data in URLs, logs, analytics, exception trackers, localStorage, cache, cookies, or sessions.
- Missing `config.filter_parameters` coverage for passwords, secrets, tokens, keys, OTP codes, certificates, and sensitive identifiers such as SSNs.
- Sensitive model attributes that should use Active Record Encryption or an equivalent encryption layer.
- Weak digests: MD5/SHA1 for passwords, tokens, or signatures.
- Custom encryption or homegrown crypto. Prefer Rails primitives, vetted gems, or platform KMS.

Before recommending `VERIFY_PEER`, identify the deployed certificate chain. Managed Redis/Postgres services may require CA configuration, plan changes, or documented accepted risk.

### A03: Injection and XSS

- SQL injection in `where`, `joins`, `order`, `reorder`, `select`, `delete_all`, `update_all`, `find_by_sql`, and `Arel.sql`.
- Raw SQL through reporting/analytics helpers such as `pluck`, `sum`, `calculate`, `group`, `having`, and geospatial query fragments when column names or SQL fragments come from params.
- LIKE queries that interpolate user input without `ActiveRecord::Base.sanitize_sql_like`.
- Sort/filter params that choose column names or directions without allowlists.
- Command injection through `eval`, `system`, `syscall`, backticks, `%x[]`, `Open3`, `exec`, `spawn`, `Process.exec`, `Process.spawn`, `IO.popen`, or shell commands. Prefer argument-array APIs such as `system(command, arg1, arg2)`.
- `Kernel#open`, bare `open`, or IO file helpers with user-controlled strings. A leading `|` can execute a command in several Ruby APIs; use `File.open`, `IO.open`, or `URI(...).open` as appropriate.
- XSS through `raw`, `.html_safe`, `<%==`, weak `sanitize`, unsafe Markdown, `simple_format`, untrusted URLs in `link_to`, or JSON embedded in scripts.
- JSON-LD and inline script breakout. Use `json_escape(object.to_json).html_safe`, then test `</script>`, apostrophes, `$`, and U+2028/U+2029.
- Unquoted HTML attributes. Attribute values that include user input must be quoted even when Rails escapes the value.
- Haml `!=` output, ERB `<%==`, `raw`, and `.html_safe` with user-controlled data.
- I18n keys ending in `_html` and translation strings containing HTML. Verify interpolated values remain escaped and developers did not add `.html_safe` to translations.
- AJAX, Turbo Stream, JavaScript, and JSON responses that interpolate user input without `j`, `json_escape`, or context-appropriate escaping.
- Custom CSS, Textile, Markdown, ActionText, or rich text rendering without a strict allowlist sanitizer. Do not rely on blacklist removal.
- SVG uploads and user HTML. Treat them as active content unless rasterized or served from an isolated origin with restrictive headers.
- Server-side template injection through `render inline:` or user-controlled template names. Do not pass request parameters into `render` template selection.
- User-controlled strings sent in emails to other users, especially free-text URLs that email clients auto-link into phishing or malware links.
- Plaintext passwords, reset tokens, API keys, or sensitive credentials sent by email.
- File upload/download path traversal: user-controlled filenames in `File.open`, `File.read`, `File.write`, `send_file`, `send_data`, ActiveStorage metadata, or export paths. Validate with allowlists, use generated storage names, and verify expanded paths stay under the expected directory.
- Response header injection: user input in `response.headers`, `Content-Disposition`, filenames, redirects, or cookies must reject CRLF and other control characters.

When one field reaches an unsafe sink, grep every view, partial, serializer, mailer, admin page, and JSON builder that renders the same field.

### A04: Insecure Design

Review business logic, not only code patterns.

- Signup, invite, password reset, account switching, support impersonation, billing, and webhook flows.
- Missing Rails `rate_limit`, Rack::Attack, or equivalent controls on login, password reset, signup, invites, magic links, unauthenticated webhooks, uploads, search, exports, and expensive background jobs.
- Configured-but-not-loaded controls. Verify gems such as `rack-attack`, `pundit`, `sidekiq`, and `doorkeeper` are installed and active at runtime.
- Provider race conditions: local state should claim work before creating Stripe/payment/email/external resources.
- Worker atomicity: avoid `SELECT pending → side effect → UPDATE`; use atomic claims or row locks.
- External side effects before durable state. Prefer an outbox pattern for email, webhooks, payments, and files.
- Business logic bugs that tools will miss. Review sensitive flows with code review, paired walkthroughs, and unit/request tests for both allowed and denied paths.
- Denial-of-service paths: expensive searches, unbounded exports, large uploads, archive extraction, regex backtracking, synchronous media processing, disk-fill paths, and endpoints that allocate memory or CPU based on user input.
- Whitelist validation for security-sensitive inputs. In Ruby regexes, prefer `\A` and `\z` over `^` and `$` so newline injection cannot bypass format checks.
- Catch-all routes such as `match ':controller(/:action(/:id))'`, public non-action controller methods, or routing that lets users choose controllers/actions/templates.

### A05: Security Misconfiguration

- `consider_all_requests_local`, web-console, rack-mini-profiler, debug logs, detailed exceptions, or schema introspection exposed outside local development.
- Missing or weakened Rails default security headers: `X-Frame-Options`, `X-XSS-Protection: 0`, `X-Content-Type-Options`, `X-Permitted-Cross-Domain-Policies`, and `Referrer-Policy`.
- Missing or weak CSP, HSTS, secure cookies, host authorization, CORS, frame protection, content-type protection, and referrer policy.
- CSP disabled, stuck in report-only without a rollout plan, using `unsafe-inline` where nonces would work, or nonce generation/caching that can leak or reuse stale nonces.
- Missing or over-broad `permissions_policy` for browser features such as camera, microphone, geolocation, USB, fullscreen, and payment.
- Host authorization missing in production or exceptions that bypass host checks for more than health checks.
- Over-broad CORS origins, methods, or credentials on API apps.
- `config.force_ssl` disabled in production, or enabled without correct TLS/proxy configuration.
- Public `.env`, database dumps, credentials, local storage, logs, or uploads.
- Sensitive files committed or served: `config/database.yml`, legacy `config/initializers/secret_token.rb`, `db/seeds.rb` with bootstrap admins/secrets, `db/development.sqlite3`, dumps, backups, or fixtures with real data.
- User uploads stored under `public/` or the web server document root where executable extensions, HTML, SVG, or scriptable files may run in the application origin.
- Image/video/archive processing without size limits, media-type validation, async processing, malware scanning where needed, zip-bomb checks, or ImageMagick/libvips hardening.
- Admin engines mounted without strong auth in staging/review apps.
- Error serializers that expose SQL errors, model internals, validation schemas, stack traces, or provider responses.

### A06: Vulnerable Components

- Run `bundle audit`, `brakeman`, JavaScript audit tooling, and container scans when available.
- Verify findings against `Gemfile.lock`, `package-lock.json`/`yarn.lock`, Docker images, and deployed versions.
- Separate runtime, build-time, dev-only, and test-only exposure.
- Review ignored Brakeman warnings and document why they remain accepted.

### A07: Identification and Authentication Failures

- Weak password policy, missing minimum length/complexity around `has_secure_password`, missing lockout/rate limit, poor reset flows, missing session regeneration after login/logout, insecure remember-me tokens.
- Sessions that store secrets, authorization decisions, credits/balances, large objects, or other mutable security state instead of server-side records.
- Missing idle and absolute session expiry for sensitive applications.
- Password or email change flows that do not require the current password or a recent strong re-authentication.
- Login and forgot-password flows that reveal whether a username or email exists.
- Login flows that do not use timing-safe password checks such as Rails `authenticate_by` or a mature auth library.
- Missing 2FA/passkeys for admins, billing users, support users, or users who can export customer data.
- Devise models missing `:validatable` while relying on `config.password_length`.
- Devise/OmniAuth callback CSRF/state, redirect validation, account linking, and tenant boundary bugs.
- Credentials stored directly in cookies or sessions.
- API tokens without expiry, rotation, scoping, or constant-time comparison.

### A08: Software and Data Integrity Failures

- `Marshal.load`, `YAML.load`, unsafe deserialization, legacy cookie serializers, and user-controlled `constantize`.
- Webhook handlers without signature validation, replay checks, idempotency, or external-ID matching.
- CI/CD without pinned actions, lockfile enforcement, or protected deploy secrets.
- Provider IDs overwritten while previous payment/upload/subscription resources are in flight.

### A09: Logging and Monitoring Failures

- Missing product-grade audit logs for admin access, auth events, 2FA changes, privilege changes, billing changes, webhook failures, rate limits, exports, and impersonation. Rails request logs alone are not enough.
- Sensitive values in logs: passwords, tokens, reset links, session cookies, Authorization headers, PII, payment data.
- Email abuse paths where unauthenticated users can send messages from a trusted domain to arbitrary recipients.
- Missing alerts for repeated login failures, webhook signature failures, admin-engine access, queue retries, and provider reconciliation failures.

### A10: SSRF

Audit user-controlled URLs passed to `Net::HTTP`, `Faraday`, `HTTParty`, `RestClient`, `URI.open`, webhooks, URL previews, imports, image fetching, or ActiveStorage attach-from-URL features.

Defenses must reject:

- Non-HTTP schemes, embedded credentials, `@` tricks, non-default ports.
- Punycode confusion, trailing dots, subdomain confusion.
- IPv6, integer/octal/hex IPv4 forms, localhost, private ranges, link-local, and metadata IPs.
- Redirects into blocked hosts.
- DNS rebinding between validation and fetch.

Use explicit timeouts, size limits, method restrictions, content-type checks, and an egress proxy for high-risk fetches.

## Verify Fixes

After recommending or applying a fix, exercise the real code path.

- Rails middleware: `bundle exec rails middleware` and a live request.
- Routes and mounted engines: capture HTTP status and auth behavior.
- Auth: test unauthenticated, wrong-user, wrong-tenant, wrong-state, and authorized paths.
- XSS: test adversarial payloads through the view or serializer.
- Webhooks: test bad signature, replay, duplicate delivery, and valid delivery.
- Jobs: test retry, idempotency, and race behavior when practical.

## Report Format

```markdown
# Rails Security Audit Report
## Project
## Stack
## Date

### Summary
- Total findings: X
- Critical: X | High: X | Medium: X | Low: X | Info: X
- Fixed: X | Deferred: X | Accepted Risk: X

#### [SEVERITY] A0X: [Title]
**File:** `path/to/file.rb:42`
**CWE:** CWE-XXX
**Disposition:** Fixed | Deferred | Accepted Risk

**Description:** [Specific vulnerability and impact]
**Evidence:** [Code, route, command output, request, or log]
**Remediation:** [Concrete code/config change]
**Verification:** [Command, request, spec, or Rails runner snippet]
**Accepted Risk Details:** [Only when accepted]

### Prioritized Remediation Plan
1. [Critical fixes]
2. [High fixes]
3. [Scheduled work]
4. [Accepted risks and re-evaluation triggers]
```

## Second Pass

Before finalizing, ask:

1. Did the fix run on the actual code path?
2. Did it add a dependency, env var, provider call, or deployment assumption?
3. Can adversarial input bypass it?
4. Did sibling routes, jobs, views, serializers, and mailers receive equivalent protection?
5. Does every finding include verification evidence?

## Boundaries

- Audit only code the user provides or authorizes.
- Flag low-confidence findings as potential.
- Prioritize auth, authorization, input handling, data access, external side effects, mounted admin surfaces, and deployment config when time is limited.
- Refuse requests to add backdoors, weaken controls, hide vulnerabilities, or attack systems outside scope.

## References

- OWASP Top 10
- OWASP Web Security Testing Guide
- Rails Security Guide
- Historical Rails 2.3 Security Guide threat model
- Saeloun Rails Security Best Practices guide
- Brakeman
- Devise, Pundit, Sidekiq, Rack::Attack, ActiveStorage, and Doorkeeper documentation
