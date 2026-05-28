---
name: incident-triage
description: "Guide rapid triage and initial response for Ruby on Rails security incidents. Use when the user mentions incident response, Rails breach, compromised app, suspicious Rails logs, hacked server, leaked credentials, unauthorized admin access, data exfiltration, malware, webhook abuse, account takeover, IOC, or indicators of compromise."
allowed-tools: Bash, Read, Grep, Glob, WebSearch
---

# Incident Triage — Rails Security Response

Guide first-response triage for Ruby on Rails application incidents. Preserve evidence, contain safely, identify scope, and produce clear next steps.

## Validation Runner Mode

Run this skill as incident validation, not education. Establish facts, preserve evidence, classify confidence, and report confirmed indicators, material unknowns, containment status, and next checks. Include timestamps, log paths, hashes, command output, and stakeholder actions.

## Priorities

1. Protect people and customers.
2. Stop active harm without destroying evidence.
3. Preserve logs, volatile data, and affected artifacts.
4. Identify root cause, scope, and affected data.
5. Document every action with UTC timestamps.

## Step 1: Classify the Rails Incident

Common Rails incident types:

- Account takeover or credential stuffing.
- Admin account compromise or impersonation abuse.
- IDOR or authorization bypass.
- SQL injection, XSS, SSRF, file upload abuse, deserialization.
- Exposed admin engines: Sidekiq, PgHero, Flipper, GoodJob, Blazer, RailsAdmin, ActiveAdmin.
- Secret leakage: `RAILS_MASTER_KEY`, `secret_key_base`, database URL, provider keys.
- Webhook abuse, payment abuse, email abuse, spam relay.
- ActiveStorage or upload malware/phishing hosting.
- Server compromise, web shell, malicious gem, CI/CD compromise.
- Data exfiltration from database, exports, logs, backups, or object storage.

Severity guide:

- **Critical:** active data exfiltration, production write access by attacker, exposed secrets with confirmed use, ransomware, payment abuse, admin compromise.
- **High:** confirmed unauthorized access, exploitable auth bypass, exposed production data, malicious code in app or CI.
- **Medium:** suspicious behavior with partial evidence, blocked attacks, sensitive logs exposed.
- **Low:** reconnaissance, failed attacks, policy violations, likely false positives.

## Step 2: Immediate Questions

Ask and record:

1. What triggered the alert?
2. Which environment: production, staging, review app, worker, CI, database, storage bucket?
3. Is the incident active now?
4. What changed recently: deploy, gem upgrade, config change, migration, new integration?
5. Which users, tenants, records, files, jobs, or providers may be affected?
6. What logs and backups are available, and how long are they retained?
7. Who owns communication, customer impact assessment, and urgent patch approval?

## Step 3: Initial Containment

Choose containment that preserves evidence and limits customer impact.

Possible Rails containment actions:

- Disable compromised accounts, API tokens, OAuth apps, and admin sessions.
- Rotate exposed credentials: `RAILS_MASTER_KEY`, provider keys, database passwords, Redis URLs, webhook secrets, cloud keys.
- Revoke sessions if `secret_key_base` or session keys are exposed.
- Disable affected feature flags, routes, jobs, or integrations.
- Block abusive IPs/user agents at WAF, CDN, load balancer, or Rack middleware.
- Pause Sidekiq queues only if jobs are causing harm; preserve queue state first.
- Put exposed admin engines behind auth/VPN or remove the mount.
- Make public buckets/private objects inaccessible when storage exposure is confirmed.

Avoid powering off hosts unless required for safety. Capture volatile state first when possible.

## Step 4: Preserve Evidence

Record UTC time before each command.

### Host and Process State

```bash
date -u
ps auxf
ss -tupn
lsof -nP
who -a
crontab -l 2>/dev/null
systemctl list-timers 2>/dev/null
```

### Rails and Deployment State

```bash
git rev-parse HEAD 2>/dev/null
git status --short 2>/dev/null
bundle exec rails runner 'puts Rails.env; puts Rails.version' 2>/dev/null
bundle exec rails routes 2>/dev/null | head -200
bundle exec rails middleware 2>/dev/null
```

### Logs to Preserve

Copy or snapshot before rotation:

```text
log/production.log
log/sidekiq.log
log/*.log
/var/log/nginx/*
/var/log/apache2/*
/var/log/auth.log
/var/log/syslog
journald exports
CDN/WAF/load balancer logs
Postgres/MySQL audit logs
Redis logs
Sidekiq retries/dead set
object storage access logs
provider dashboards: Stripe, email, auth, SSO
CI/CD workflow logs
```

Hash preserved evidence:

```bash
shasum -a 256 <file>
```

## Step 5: Rails-Focused Initial Analysis

### Authentication and Account Activity

Look for:

- Login bursts, password reset bursts, repeated failures.
- Admin logins from new IPs or countries.
- Session reuse after password change.
- OAuth/SSO callback anomalies.
- New admin users, role changes, impersonation events.

### Web Requests and Errors

Search logs for:

```text
Completed 500
ActionController::RoutingError
ActionController::InvalidAuthenticityToken
ActiveRecord::StatementInvalid
PG::SyntaxError
Mysql2::Error
NoMethodError
NameError
Started POST
Started DELETE
/users/password
/admin
/sidekiq
/rails/active_storage
/webhooks
```

Review params carefully. Redact secrets in reports.

### Database and Data Access

Check for:

- Unusual exports, reports, bulk downloads, API pagination, or search queries.
- Access to many tenants by one user or token.
- Rows created or modified near the incident time: users, roles, API tokens, webhooks, feature flags, payment records, exports.
- Suspicious SQL errors that may indicate injection attempts.

Use read-only queries. Prefer snapshots for deeper analysis.

### Jobs, Queues, and Providers

Inspect:

- Sidekiq retries/dead jobs.
- Jobs that sent emails, webhooks, exports, invoices, refunds, or file processing.
- Webhook signature failures and replay attempts.
- Provider dashboards for matching timestamps.

### File and Code Integrity

Check recently modified files:

```bash
find . -type f -mtime -7 -not -path './tmp/*' -not -path './log/*' -print
```

Look for:

- Modified initializers, routes, controllers, views, jobs, mailers, rake tasks.
- Unexpected files in `public/`, `tmp/`, upload directories, or shared release dirs.
- New gems, Git dependencies, or lockfile changes.
- Shell commands in deploy scripts or CI workflows.

## Step 6: IOC Extraction

Document indicators:

| Type | Examples |
|------|----------|
| Accounts | user IDs, admin IDs, API token IDs |
| Network | source IPs, ASNs, user agents, domains |
| Rails | controller/action, route, params shape, request IDs |
| Files | paths, uploads, hashes |
| Jobs | job class, jid, queue, args hash |
| Database | table, record IDs, tenant IDs |
| Cloud | access key ID, bucket object key, log stream |
| Provider | Stripe event ID, webhook ID, email message ID |

## Step 7: Recovery and Follow-Up

Recommend recovery actions tied to evidence:

- Patch vulnerable code and add regression tests.
- Estimate and communicate the security update timeline to stakeholders when a vulnerable dependency or production exposure affects customers.
- Rotate affected secrets and invalidate sessions/tokens.
- Rebuild hosts/images from trusted sources if compromise reached the server or CI.
- Review logs for the full retention window.
- Notify legal/compliance if regulated data may be affected.
- Add monitoring for the exploited path.
- Run a post-incident Rails security review focused on root cause and sibling code paths.

## Output Format

```markdown
# Rails Incident Triage Report
## Incident ID
## Date/Time UTC
## Severity
## Classification
## Status

### Executive Summary
[Short factual summary]

### Affected Systems and Tenants
| System/Tenant | Role | Status | Evidence |
|---------------|------|--------|----------|

### Timeline
| Time UTC | Event | Source | Notes |
|----------|-------|--------|-------|

### Indicators of Compromise
| Type | Value | Context | Confidence |
|------|-------|---------|------------|

### Containment Actions
| Time UTC | Action | Actor | Result | Evidence Preserved? |
|----------|--------|-------|--------|---------------------|

### Evidence Preserved
| Item | Location | SHA256 | Notes |
|------|----------|--------|-------|

### Current Assessment
- Root cause hypothesis:
- Data exposure assessment:
- Active risk:
- Unknowns:

### Next Steps
1. [Immediate]
2. [Within 24 hours]
3. [Follow-up]

### Escalation Checklist
- [ ] Management notified
- [ ] Legal/privacy notified if data exposure is possible
- [ ] Customer notification assessment started
- [ ] Cloud/provider support engaged if needed
- [ ] External IR counsel/vendor considered
- [ ] Customer/client support obligations and notification timelines reviewed
```

## Boundaries

- Focus on defense, containment, and evidence.
- Do not recommend retaliation or hacking back.
- Do not modify logs, erase artifacts, or cover up incidents.
- If a containment action could break production, state the risk and ask for approval.
- Refuse requests to hide compromise, tamper with evidence, or access unauthorized systems.

## References

- NIST SP 800-61
- SANS Incident Handler's Handbook
- MITRE ATT&CK
- Rails Security Guide
- OWASP Web Security Testing Guide
