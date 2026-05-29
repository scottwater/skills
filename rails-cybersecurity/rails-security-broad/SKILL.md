---
name: rails-security-broad
description: "Run a broader repository-only Rails security review across the core codebase lenses plus cloud/platform/IaC/configuration review for weekly, branch, PR, last-N-commit, or GitHub code review security validation with repository configuration coverage."
allowed-tools: Read, Grep, Glob, Bash
---

# Rails Security Broad

Run a broader repository-only Rails security review.

Use this skill for recurring GitHub/codebase review when the user wants the routine core Rails security review plus repository evidence for cloud, platform, deployment, CI/CD, and infrastructure configuration. It does not assume access to production servers, live domains, cloud accounts, server logs, or forensic images.

If the user wants the fastest routine review, use `rails-cybersecurity/rails-security-core`. If the user asks for one lens only, use the relevant specialist directly.

## Review Lenses

1. `rails-cybersecurity/rails-security-core` logic:
   - `rails-cybersecurity/rails-auth-audit`
   - `rails-cybersecurity/owasp-audit`
   - `rails-cybersecurity/dependency-audit`
   - `rails-cybersecurity/prompt-injection`
2. `rails-cybersecurity/cloud-audit` in repository-only mode:
   - Rails environment config, storage config, cable config, credentials references, Docker, Procfile, Kamal, Terraform, Kubernetes, CI/CD, GitHub Actions, deployment descriptors, and operational/security configuration available in the repo.

Do not run routine recon, OSINT, incident triage, or disk forensics as part of this review. Those skills require external target, incident, log, evidence-image, or public-intelligence context that is not available in a normal code scan.

## Authorization And Scope

Confirm the user owns, maintains, or is authorized to review the repository, branch, pull request, diff, or commits. If the request implies live scanning, production access, cloud credentials, external targets, or server logs, ask for explicit authorization and scope before using them. For normal code review, treat those live/environment checks as unavailable or not in scope.

First establish the comparison scope and report it briefly.

If the user provides an explicit range, pending-change request, commit count, branch, PR, or date range, resolve that scope directly. If no comparison scope is provided:

1. If the repo has tracked pending changes, validate pending tracked changes against `HEAD`.
2. Otherwise compare the current branch against `main` using the merge-base range.
3. If `main` is unavailable locally, try `origin/main` and say which base was used.
4. If no useful diff is available, validate the current checkout as a whole-repo review.

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

# Last N commits
git diff --name-status HEAD~N..HEAD
git diff --stat HEAD~N..HEAD
git log --oneline HEAD~N..HEAD

# Specific range
git diff --name-status abc123..def456
git diff --stat abc123..def456
```

If the requested scope is ambiguous, ask one short clarifying question. Otherwise choose the most likely range, state it, and proceed.

## Review Flow

1. Resolve the range once.
2. Inspect the changed file list, diff stat, and commit summary.
3. Prepare a resolved security context packet for all lenses.
4. Run the core Rails security lenses and the repository-only cloud/platform lens in parallel when the agent harness supports separate agents/skills. If not, run them sequentially yourself using each specialist's checklist.
5. Merge findings into one report, deduplicating overlap and preserving the strongest severity.
6. Separate repository-proven findings from live-environment unknowns.
7. Do not summarize every changed file. Only report evidence-backed failures, material unknowns, and high-value validation gaps.

Useful discovery commands:

```sh
git diff --name-status <range>
git diff --stat <range>
git log --oneline <range>

# Core Rails/code security surfaces
git diff <range> -- app/controllers app/models app/policies app/views app/helpers app/jobs app/mailers app/channels app/graphql lib config db
git diff <range> -- app/javascript app/assets app/frontend frontend src components pages
git diff <range> -- Gemfile Gemfile.lock package.json package-lock.json yarn.lock pnpm-lock.yaml bun.lockb
git diff <range> -- spec/requests spec/controllers spec/policies spec/system spec/features test

# Repository platform/config surfaces
git diff <range> -- config/environments config/initializers config/storage.yml config/cable.yml config/database.yml config/credentials.yml.enc config/master.key config/ci.rb
git diff <range> -- Dockerfile docker-compose.yml docker-compose*.yml .dockerignore Procfile app.json render.yaml fly.toml railway.json heroku.yml
git diff <range> -- config/deploy config/deploy.yml config/deploy.* config/kamal deploy kamal.yml
git diff <range> -- .github/workflows .gitlab-ci.yml .circleci buildkite Jenkinsfile
git diff <range> -- '*.tf' terraform infrastructure infra k8s kubernetes helm charts '*.yaml' '*.yml'
```

## Specialist Context Packet

When delegating to a specialist, pass the resolved scope as authoritative so the child skill does not reinterpret it:

```md
Resolved Rails security context:

Range: `<range or whole repository>`
Scope source: <user request or default>
Review mode: codebase/diff and repository configuration only; no live server, production logs, cloud credentials, domain, external scan, or forensic image unless explicitly provided and authorized.

Changed files:
<git diff --name-status output>

Diff stat:
<git diff --stat output>

Commit summary:
<git log --oneline output, if applicable>

Your focus:
<core Rails security | repository-only cloud/platform/configuration> only.

Report only evidence-backed security failures, material unknowns, and high-value validation gaps introduced or affected by this scope.
```

## Core Rails Security Lenses

Run or simulate `rails-cybersecurity/rails-security-core`, covering:

- Authentication and authorization: protected routes, policies, tenants, roles, IDOR, sessions, tokens, admin/support/billing/export flows, and denied-path tests.
- OWASP Rails appsec: XSS, SQL injection, SSRF, CSRF, redirects, file handling, command execution, unsafe rendering, headers, cookies, CORS, CSP, and Rails security defaults.
- Dependencies and supply chain: Rails/Ruby/gem/JS/package changes, lockfiles, scanners, CI security checks, new packages, pinned actions/images, and patch process evidence.
- Prompt injection and AI security: AI/LLM/RAG/agent/MCP features, prompt construction, RAG scoping, tool permissions, tenant leakage, model output sinks, memory, and automation boundaries.

## Repository-Only Cloud/Platform Lens

Use `rails-cybersecurity/cloud-audit` in repository-only mode to validate:

- Rails production/staging environment config, SSL, hosts, cookies, logging, cache/session/cable/storage settings, credentials references, and secret-handling patterns.
- ActiveStorage bucket configuration, public/private separation signals, signed URL expiry, direct upload assumptions, CORS references, and provider configuration present in code.
- CI/CD workflows, deploy descriptors, Docker/Kamal/Heroku/Render/Fly/Kubernetes/Terraform evidence, pinned actions/images, untrusted PR handling, and secret exposure risks.
- Databases, Redis, queues, admin dashboards, job UIs, health checks, and operational surfaces as represented in repository config/routes/IaC.
- Monitoring, security tooling, dependency alerts, scanner triage, and incident-readiness hooks available from repository evidence.

Mark these as **Unknown** or **Not In Scope**, not confirmed failures, unless repository evidence proves the issue:

- Actual cloud IAM policy state.
- Actual bucket/object ACLs.
- Actual database/Redis network exposure.
- Live WAF/CDN/rate-limit configuration.
- Server patch level and SSH hardening.
- Production logs, audit trails, and runtime alerts.
- Domain DNS, TLS certificates, and external attack surface.

## Output Format

Start with the comparison range used and review mode. Then list only actionable findings and material unknowns.

```md
# Rails Security Broad Report

Scope: `<range or repository>`
Review mode: codebase/diff plus repository configuration only
Date: `<date>`

## Executive Summary
- Critical: X | High: X | Medium: X | Low: X | Unknown: X
- Highest-risk gaps: [short list]

## Findings

### High: GitHub Action Runs Untrusted PR Code With Secrets
Status: Fail
Lens: Repository Platform Configuration
Evidence: `.github/workflows/deploy.yml:12`, `.github/workflows/deploy.yml:29`

[Specific risk and why it matters.]

Required validation:
- [specific repo/CI checks]

Recommended fix:
- [specific workflow/config direction]

## Unknowns / Not In Scope
- Live cloud IAM, runtime bucket ACLs, production logs, DNS/TLS, external scanning, server patch levels, and forensic evidence were not available unless explicitly provided.

## Suggested Validation Commands
- [commands/specs to run next]
```

Severity guide:

- **Critical:** confirmed auth bypass, cross-tenant exposure, exposed production secrets, reachable RCE, unsafe file execution, actively exploitable runtime dependency, unsafe CI/deploy secret exposure, unsafe AI tool action that can mutate or expose tenant data.
- **High:** likely authz gap, missing policy scope on sensitive data, dangerous XSS/SQL/SSRF/file sink, CSRF on state-changing cookie-auth path, unsupported Rails/Ruby with known security exposure, unsafe cloud/deploy config proven by repo evidence.
- **Medium:** missing lower-permission tests, scanner/tooling gaps, weak headers/CSP/CORS, rate-limit gaps, unsafe upload processing, logging/PII risk, repository config unknowns that block production assurance.
- **Low:** hardening gaps, documentation/process gaps, low-risk outdated packages, optional defense-in-depth.
- **Unknown:** material control not provable from repository evidence.

## What Not To Do

- Do not run live scans, cloud CLI commands, production commands, or external probing unless explicitly authorized.
- Do not require a domain, server logs, cloud account, or forensic image for routine code review.
- Do not run recon, OSINT, incident triage, or disk forensics as part of this routine review.
- Do not report live-environment assumptions as confirmed findings when only repository evidence is available.
- Do not list every changed file.
- Do not treat scanner warnings as vulnerabilities until applicability is checked.
