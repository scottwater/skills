---
name: recon
description: "Perform authorized reconnaissance and attack surface enumeration for Ruby on Rails applications. Use when the user mentions recon, reconnaissance, attack surface, Rails app mapping, route discovery, subdomain enumeration, exposed admin panels, public assets, ports, fingerprinting, or bug bounty scoping for a Rails target."
allowed-tools: Bash, Read, WebSearch, WebFetch
---

# Recon — Rails Application Attack Surface Mapping

Map an authorized Ruby on Rails application's external and code-adjacent attack surface. Treat recon as the first pass of a Rails security review: find entry points, trust boundaries, exposed services, framework clues, and risky operational surfaces.

## Validation Runner Mode

Run this skill as validation, not education. Resolve scope, gather passive and authorized active evidence, and report exposed assets, Rails signals, risky surfaces, material unknowns, and next validation checks. Include commands, URLs, headers, routes, or source references for each finding.

## Authorization Check

Before running commands, confirm:

1. The user has written authorization for the target.
2. The target, domains, subdomains, IPs, environments, and rate limits are in scope.
3. Active scanning is allowed.

If scope is unclear, ask. Refuse unauthorized recon, mass scanning, or requests aimed at third-party systems without permission.

## Phase 1: Passive Recon

Gather information without sending traffic to the target application.

### Domain and DNS

```bash
dig A <domain>
dig AAAA <domain>
dig MX <domain>
dig TXT <domain>
dig NS <domain>
whois <domain>
```

Check certificate transparency for app, API, staging, review, and admin subdomains:

```bash
curl -s "https://crt.sh/?q=%25.<domain>&output=json" | jq -r '.[].name_value' | sort -u
```

Look for Rails deployment patterns:

- `app`, `api`, `admin`, `staging`, `demo`, `review`, `sidekiq`, `jobs`, `status`, `assets`, `cdn`.
- Heroku, Render, Fly.io, Hatchbox, Kubernetes ingress, CloudFront, Fastly, Cloudflare, S3, or GCS hostnames.

### Public Code and Secret Exposure

Search public repositories, issues, packages, and documentation for:

- `Gemfile`, `Gemfile.lock`, `.ruby-version`, `config/routes.rb`, `config/storage.yml`, `config/database.yml`.
- Rails credentials mistakes: `RAILS_MASTER_KEY`, `secret_key_base`, `config/master.key`, `.env`, API keys.
- Internal routes, admin paths, Sidekiq/PgHero/Flipper mounts, webhook endpoints, ActiveStorage URLs.

Use targeted searches:

```text
site:github.com <org> Gemfile.lock rails
site:github.com <domain> RAILS_MASTER_KEY OR secret_key_base
site:<domain> filetype:pdf OR filetype:xlsx OR filetype:csv
```

### Historical and Search Data

Review Wayback Machine and search results for removed endpoints:

- Old admin paths.
- Legacy API versions.
- Exposed debug pages.
- Direct upload, import, export, webhook, and password reset flows.
- Asset filenames that reveal framework or gem versions.

## Phase 2: Safe HTTP Fingerprinting

Use low-volume requests first. Capture headers and cookies.

```bash
curl -i https://<host>/
curl -I https://<host>/
```

Look for:

- Rails cookies: `_app_session`, signed/encrypted cookie shape, missing `Secure`, `HttpOnly`, or `SameSite`.
- Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy.
- Cache behavior on authenticated or sensitive paths.
- Error pages, debug pages, Rails exception output, stack traces, or framework banners.
- CSRF tokens in forms and Turbo/Hotwire behavior.

Probe common Rails and operations paths only when in scope:

```text
/rails/active_storage/blobs/redirect/...
/rails/active_storage/direct_uploads
/rails/mailers
/rails/info/routes
/sidekiq
/admin
/admin/users
/flipper
/pghero
/good_job
/blazer
/graphql
/api
/api/v1
/up
/health
/status
```

Do not brute force by default. Ask before content discovery.

## Phase 3: Active Recon

Run active checks only after the user confirms authorization.

### Network and Service Mapping

```bash
nmap -sV -sC -oN nmap-rails-target.txt <host>
```

Start with standard web ports. Expand only if scope allows it. For cloud apps, prioritize HTTP behavior over broad port scans.

### Web Content Discovery

If allowed, use a small Rails-aware wordlist before any large scan. Include:

```text
admin
users/sign_in
users/password/new
session/new
rails/active_storage/direct_uploads
sidekiq
flipper
pghero
good_job
blazer
letter_opener
api
api/v1
graphql
webhooks
exports
imports
```

Rate-limit discovery. Stop if the app degrades or the program rules prohibit it.

### Rails Workflow Mapping

Map the app's exposed workflows:

- Authentication and signup.
- Password reset, invitation, email confirmation.
- Tenant/account switching.
- File upload and ActiveStorage direct upload.
- Webhooks and callbacks.
- Imports, exports, reports, search.
- Billing and subscription flows.
- Admin and support impersonation features.
- APIs, GraphQL, JSON endpoints, ActionCable.

For each workflow, record inputs, IDs, redirects, auth state, tenant boundaries, and side effects.

## Phase 4: Analysis

Prioritize findings a Rails researcher would test next:

1. Exposed admin engines or debug routes.
2. Missing auth on operations surfaces.
3. Weak session cookie attributes or host/SSL configuration.
4. IDOR-prone routes with numeric IDs or tenant objects.
5. File upload and ActiveStorage exposure.
6. Webhook endpoints without clear signature constraints.
7. Open redirects in `return_to`, `next`, `redirect`, or `continue` params.
8. Search, sort, filter, import, and export features that may hit SQL, command, or SSRF sinks.
9. Staging/review apps with production data or weak auth.

## Output Format

```markdown
# Rails Recon Report
## Target
## Confirmed Scope
## Date

### External Surface
| Host | Purpose | Provider/CDN | Notes |
|------|---------|--------------|-------|

### Rails Signals
| Signal | Evidence | Risk |
|--------|----------|------|

### Routes and Workflows
| Workflow | URL(s) | Auth Required | Inputs | Notes |
|----------|--------|---------------|--------|-------|

### Exposed Operations Surfaces
| Surface | URL | Auth State | Risk |
|---------|-----|------------|------|

### Security Header and Cookie Review
| Control | Observed | Concern |
|---------|----------|---------|

### Prioritized Research Leads
1. [Highest-value next test]
2. [Next]
```

## Boundaries

- Stay inside confirmed scope.
- Rate-limit active checks.
- Log commands and timestamps.
- Do not bypass authentication unless the engagement permits it.
- Stop and notify the user if you find evidence of active compromise.
- Provide defensive findings and next steps, not unauthorized exploit playbooks.

## References

- OWASP Web Security Testing Guide
- OWASP Rails Security Cheat Sheet
- Rails Security Guide
- PTES Reconnaissance guidance
