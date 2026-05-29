---
name: rails-security-core
description: "Run routine codebase-focused Rails security review across authentication/authorization, OWASP appsec, dependency/supply-chain, and prompt-injection lenses for recurring PR, branch, last-N-commit, or GitHub code review security validation."
allowed-tools: Read, Grep, Glob, Bash
---

# Rails Security Core

Run a routine Rails security review for codebase changes.

Use this skill for frequent GitHub/codebase review, such as daily, weekly, pull-request, branch, pending-change, or last-N-commit checks. It does not assume access to production servers, live domains, cloud accounts, server logs, or forensic images.

If the user asks for one lens only, use the relevant specialist directly:

- `rails-cybersecurity/rails-auth-audit`: authentication, authorization, policies, roles, tenants, sessions, tokens, and controller access.
- `rails-cybersecurity/owasp-audit`: Rails/Ruby/JavaScript appsec checks including access control, XSS, SQL injection, CSRF, SSRF, file handling, redirects, logging, and misconfiguration.
- `rails-cybersecurity/dependency-audit`: Ruby, Rails, gem, JavaScript package, lockfile, CI, tooling, and supply-chain review.
- `rails-cybersecurity/prompt-injection`: Rails AI, LLM, RAG, agent, MCP, automation, tool-use, tenant-leakage, and output-handling review.

The specialist skills must remain independently runnable. This skill resolves the shared scope, runs or simulates each specialist lens, and merges the results.

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
3. Prepare a resolved security context packet for the specialists.
4. Run the four specialist lenses in parallel when the agent harness supports separate agents/skills. If not, run the lenses sequentially yourself using each specialist's checklist.
5. Merge findings into one report, deduplicating overlap and preserving the strongest severity.
6. Report only evidence-backed failures, material unknowns, and high-value validation gaps. Do not summarize every changed file.

Useful discovery commands:

```sh
git diff --name-status <range>
git diff --stat <range>
git log --oneline <range>

git diff <range> -- app/controllers app/models app/policies app/views app/helpers app/jobs app/mailers app/channels app/graphql lib config db
git diff <range> -- app/javascript app/assets app/frontend frontend src components pages
git diff <range> -- Gemfile Gemfile.lock package.json package-lock.json yarn.lock pnpm-lock.yaml bun.lockb
git diff <range> -- .github/workflows .gitlab-ci.yml config/ci.rb Dockerfile docker-compose.yml Procfile

git diff <range> -- spec/requests spec/controllers spec/policies spec/system spec/features test
```

## Specialist Context Packet

When delegating to a specialist, pass the resolved scope as authoritative so the child skill does not reinterpret it:

```md
Resolved Rails security context:

Range: `<range or whole repository>`
Scope source: <user request or default>
Review mode: codebase/diff only; no live server, production logs, cloud credentials, domain, or forensic image unless explicitly provided and authorized.

Changed files:
<git diff --name-status output>

Diff stat:
<git diff --stat output>

Commit summary:
<git log --oneline output, if applicable>

Your focus:
<auth/authz | OWASP appsec | dependency/supply chain | prompt injection> only.

Report only evidence-backed security failures, material unknowns, and high-value validation gaps introduced or affected by this scope.
```

## Specialist Lenses

### Authentication And Authorization

Use `rails-cybersecurity/rails-auth-audit` to validate:

- Authentication requirements on protected routes and entry points.
- Authorization and policy coverage for controllers, APIs, GraphQL, jobs, mailers, exports, mounted engines, and custom actions.
- Tenant/account scoping, IDOR candidates, policy scopes, role transitions, admin/support/billing/export flows, and lower-permission test coverage.
- Session rotation, expiry, remember-me behavior, reset/invitation/magic-link tokens, API tokens, SSO/OAuth callbacks, rate limits, lockout, and audit logging.

### OWASP Rails AppSec

Use `rails-cybersecurity/owasp-audit` to validate:

- Rails/Ruby/JavaScript sinks for XSS, SQL injection, SSRF, unsafe redirects, unsafe file handling, command execution, deserialization, header injection, and logging exposure.
- CSRF, Turbo/custom JavaScript token handling, state-changing GET routes, CORS, CSP, host authorization, secure cookies, and Rails security defaults.
- Strong params / `params.expect`, privilege fields, foreign keys, tenant IDs, unsafe rendering, unsafe `_html` translations, rich text, uploads, exports, and reporting queries.
- Missing specs that should prove denied paths, adversarial input, tenant isolation, and sibling route coverage.

### Dependencies And Supply Chain

Use `rails-cybersecurity/dependency-audit` to validate:

- Rails, Ruby, Rack, Puma/Passenger, gems, JavaScript packages, lockfiles, containers, CI, and security tooling changes.
- Brakeman, bundler-audit, importmap audit, npm/yarn/pnpm audit, RuboCop Security cops, dependency alert posture, and false-positive tracking.
- New gems/packages for necessity, maintenance, license, native extensions, install scripts, transitive risk, and security-sensitive runtime exposure.
- CI/CD safety, pinned actions/images, lockfile enforcement, and emergency patch process evidence available in the repository.

### Prompt Injection And AI Security

Use `rails-cybersecurity/prompt-injection` to validate:

- AI/LLM/RAG/agent/MCP/automation features in Rails, Ruby, JavaScript, Stimulus, React, jobs, services, and integrations.
- Prompt construction, untrusted content in prompts, RAG retrieval scoping, tool/function permissions, background-job identity, tenant leakage, model output sinks, and follow-up tool calls.
- Unsafe rendering of model output in HTML/Markdown/ActionText/JSON/email, prompt leakage, memory isolation, and audit logs for sensitive AI actions.
- If no AI/LLM/agent functionality is present or affected, say so with the evidence checked rather than reporting a finding.

## Output Format

Start with the comparison range used and review mode. Then list only actionable findings and material unknowns.

```md
# Rails Security Core Report

Scope: `<range or repository>`
Review mode: codebase/diff only
Date: `<date>`

## Executive Summary
- Critical: X | High: X | Medium: X | Low: X | Unknown: X
- Highest-risk gaps: [short list]

## Findings

### High: Cross-Tenant Project Lookup Is Not Policy Scoped
Status: Fail
Lens: Authentication And Authorization
Evidence: `app/controllers/projects_controller.rb:42`, `app/policies/project_policy.rb:18`

[Specific risk and why it matters.]

Required validation:
- [specific request/policy/spec/manual checks]

Recommended fix:
- [specific code/config/test direction]

## Unknowns / Not In Scope
- Live server behavior, production logs, domains, cloud account state, and forensic evidence were not available unless explicitly provided.

## Suggested Validation Commands
- [commands/specs to run next]
```

Severity guide:

- **Critical:** confirmed auth bypass, cross-tenant exposure, exposed production secrets, reachable RCE, unsafe file execution, actively exploitable runtime dependency, unsafe model/tool action that can mutate or expose tenant data.
- **High:** likely authz gap, missing policy scope on sensitive data, dangerous XSS/SQL/SSRF/file sink, CSRF on state-changing cookie-auth path, unsupported Rails/Ruby with known security exposure, unsafe AI tool boundary.
- **Medium:** missing lower-permission tests, scanner/tooling gaps, weak headers/CSP/CORS, rate-limit gaps, unsafe upload processing, logging/PII risk, prompt-injection hardening gaps.
- **Low:** hardening gaps, documentation/process gaps, low-risk outdated packages, optional defense-in-depth.
- **Unknown:** material control not provable from repository evidence.

## What Not To Do

- Do not run live scans, cloud CLI commands, production commands, or external probing unless explicitly authorized.
- Do not require a domain, server logs, cloud account, or forensic image for routine code review.
- Do not list every changed file.
- Do not report speculative issues as confirmed findings.
- Do not treat scanner warnings as vulnerabilities until applicability is checked.
- Do not ignore prompt-injection review just because AI functionality is not obvious; first search for AI/LLM/agent patterns, then mark not present if evidence supports that.
