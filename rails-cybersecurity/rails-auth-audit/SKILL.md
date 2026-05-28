---
name: rails-auth-audit
description: "Audit Ruby on Rails authentication and authorization implementations. Use when the user mentions Rails auth audit, authorization review, Pundit, Action Policy, CanCanCan, Devise, Rodauth, policy coverage, controller access, IDOR, tenant permissions, admin access, API token access, or wants to verify routes and controllers enforce the expected user roles and ownership rules."
allowed-tools: Read, Grep, Glob, Bash
---

# Rails Auth Audit — Authentication and Authorization Review

Audit a Ruby on Rails application's authentication and authorization setup. Verify that controllers, APIs, jobs, GraphQL resolvers, mounted engines, and policies enforce the expected access rules.

## Validation Runner Mode

Run this skill as validation, not education. Resolve scope, inspect evidence, and report only confirmed failures, material unknowns, and concrete validation gaps. Include file paths, routes, policies, roles, specs, or request examples for each finding. Do not explain auth concepts unless the user asks.

## Authorization Check

Confirm the user owns, maintains, or is authorized to review the application. If scope is unclear, ask before auditing. Provide defensive findings, tests, and remediation. Do not help bypass access controls on unauthorized systems.

## Goals

Answer these questions with evidence:

1. Who can authenticate, and how?
2. Which routes require authentication?
3. Which roles, tenants, or ownership rules control each action?
4. Which policy framework enforces those rules: Pundit, Action Policy, CanCanCan, or custom code?
5. Do controller actions, policy methods, and tests match the intended access model?
6. Can a user access another user's or tenant's records by changing IDs, params, tokens, or routes?

## Step 1: Identify the Auth Stack

Inspect dependencies and initializers:

```bash
grep -n "bcrypt\|devise\|rodauth\|sorcery\|clearance\|authlogic\|omniauth\|warden\|doorkeeper\|pundit\|action_policy\|cancancan\|cancan\|webauthn\|rotp" Gemfile Gemfile.lock 2>/dev/null

grep -RIn "has_secure_password\|authenticate_by\|start_new_session\|resume_session\|Current\.session\|Devise\|Rodauth\|Sorcery\|Clearance\|Authlogic\|OmniAuth\|Doorkeeper\|Pundit\|ActionPolicy\|CanCan\|CanCanCan\|rate_limit\|webauthn\|passkey\|otp\|two_factor" app/ config/ lib/ 2>/dev/null
```

Document:

- Authentication library and user models, including Rails 8 generated authentication if present: `app/controllers/concerns/authentication.rb`, `SessionsController`, `PasswordsController`, `Current`, `Session`, and `User`.
- Session, remember-me, password reset, signup, invitation, SSO, OAuth, MFA, API token, token-only API, simultaneous-session, and service-account flows.
- Authorization library and policy locations.
- Role and tenant models: `User`, `Account`, `Organization`, `Team`, `Membership`, `Role`, `Permission`.
- Admin and support impersonation paths.

## Step 2: Build a Route and Controller Inventory

List routes and controller actions:

```bash
bundle exec rails routes 2>/dev/null || bin/rails routes
find app/controllers -type f -name "*_controller.rb" | sort
```

For each controller, inspect:

```bash
grep -RIn "before_action\|prepend_before_action\|skip_before_action\|authenticate_\|current_user\|current_account\|authorize\|authorize!\|authorize_resource\|load_and_authorize_resource\|allowed_to?\|authorized_scope\|policy_scope\|skip_authorization\|skip_policy_scope" app/controllers app/graphql app/channels app/jobs app/mailers 2>/dev/null
```

Include non-controller entry points:

- API controllers and JSON endpoints.
- GraphQL queries and mutations.
- ActionCable channels.
- ActiveJob and Sidekiq jobs that mutate tenant data.
- Mailers that reveal data.
- Webhooks and callbacks.
- Mounted engines: Sidekiq, PgHero, Flipper, GoodJob, Blazer, RailsAdmin, ActiveAdmin, Avo, Administrate.

## Step 3: Verify Authentication Controls

Check that authentication works as intended:

- Protected controllers require a logged-in user or valid API token.
- Public routes are intentionally public: home, login, signup, password reset, health checks, webhooks.
- Rails 8 generated authentication code has been reviewed like application code, including sessions, password reset, and remember-me behavior.
- `has_secure_password` uses `bcrypt`, and the app adds its own minimum password length/complexity rules because Rails only enforces presence on create, max 72 bytes, and confirmation.
- Login code uses Rails `authenticate_by` or another timing-safe password verification path.
- Sessions regenerate with `reset_session`, Rails generated `start_new_session_for`, or equivalent after login, privilege elevation, and logout, and old sessions/tokens become invalid when expected.
- Sessions have idle and absolute expiry appropriate to the app's sensitivity.
- Sessions do not store secrets, balances, authorization decisions, large objects, or mutable business state that belongs in server-side records.
- Cookie-backed sessions do not expose sensitive values or permit replay of business state.
- Signed/encrypted cookie rotations, salts, ciphers, and digest changes have a planned migration and removal window.
- `skip_before_action` is narrow and documented.
- API authentication rejects missing, malformed, expired, revoked, and wrong-scope tokens.
- Token-only API controllers can skip cookie CSRF only when cookies are not accepted for authentication on those paths. Mixed cookie/token authentication still needs CSRF protection on cookie-authenticated paths.
- Session cookies use `Secure`, `HttpOnly`, and appropriate `SameSite` settings.
- Password reset, invitation, activation, and magic-link tokens expire, cannot be reused, and reject blank or missing token parameters. Rails generated reset links default to 15 minutes unless configured otherwise.
- Login, forgot-password, activation, confirmation, unlock, and reset flows use generic responses that do not reveal whether an email, username, or token exists.
- Login, password reset, invite, signup, activation, and magic-link endpoints have Rails `rate_limit`, Rack::Attack, Devise Lockable, honeypot/negative CAPTCHA, CAPTCHA after repeated failures, or equivalent abuse controls.
- CSRF failures clear persistent remember-me or authentication cookies that would otherwise survive invalid token errors.
- Remember-me tokens rotate or revoke correctly.
- The app limits or at least surfaces simultaneous active sessions per account for sensitive users.
- SSO/OAuth callbacks validate state, redirect targets, account linking, and tenant membership.
- Password changes, email changes, MFA changes, and credential recovery require the current password or recent strong re-authentication.
- Password-change notifications and email-change notifications go to the previous verified address where appropriate.
- The app never sends plaintext passwords, password hashes, reset tokens, session tokens, or API keys by email.
- Account recovery does not rely on security questions with reusable or publicly discoverable answers.
- Admin, billing, export, and support impersonation workflows require strong authorization, audit logging, and 2FA or passkeys where practical.

For Devise, verify model modules match policy assumptions:

- `:validatable` if relying on `config.password_length`.
- `:lockable` or equivalent rate limiting if brute-force risk matters.
- `:timeoutable` for sensitive applications.
- `:confirmable` or `:reconfirmable` where email ownership matters.
- `:omniauthable` callback protections.
- 2FA, WebAuthn/passkey, or OTP controls for admins and users who can expose customer data.
- `config.paranoid`, `:confirmable`, `reconfirmable`, password-change notifications, and session-limit features are enabled when the app's risk profile calls for them.

## Step 4: Verify Authorization Framework Coverage

### Pundit

Look for:

```bash
grep -RIn "include Pundit\|Pundit::Authorization\|authorize \|policy_scope\|verify_authorized\|verify_policy_scoped\|skip_authorization\|skip_policy_scope" app/ config/ 2>/dev/null
find app/policies -type f -name "*.rb" 2>/dev/null
```

Check:

- `ApplicationPolicy` defaults deny access.
- Each protected action calls `authorize` or uses an enforced wrapper.
- Index/list actions use `policy_scope`.
- `verify_authorized` and `verify_policy_scoped` run where practical.
- `skip_authorization` and `skip_policy_scope` are rare, intentional, and tested.
- Custom controller actions have matching policy methods.
- Policy checks use the same actor and tenant context as the request.
- Policy scopes cannot return records from another tenant.

### Action Policy

Look for:

```bash
grep -RIn "ActionPolicy\|authorize!\|allowed_to?\|authorized_scope\|policy_for\|pre_check\|scope_for\|authorize :" app/ config/ 2>/dev/null
find app/policies -type f -name "*.rb" 2>/dev/null
```

Check:

- Controllers include the expected Action Policy behavior.
- Actions call `authorize!` or a project wrapper before exposing or mutating data.
- Collection queries use `authorized_scope` or an equivalent tenant-safe scope.
- `allowed_to?` only controls presentation unless server-side authorization also runs.
- Policy pre-checks do not accidentally grant broad admin or owner access.
- Policy context includes `user`, `account`, tenant, token scope, or role data as needed.
- Framework verification hooks are enabled if the app uses them.

### CanCanCan

Look for:

```bash
grep -RIn "CanCan\|load_and_authorize_resource\|authorize!\|can?\|cannot\|accessible_by\|skip_authorization_check\|Ability" app/ config/ 2>/dev/null
```

Check:

- `Ability` starts from least privilege.
- Controllers use `load_and_authorize_resource`, `authorize!`, or an equivalent wrapper.
- Collection queries use `accessible_by` or a tenant-safe scope.
- Custom actions map to explicit abilities.
- `can?` in views does not replace server-side checks.
- `skip_authorization_check` is rare, intentional, and tested.
- Nested resources load through the current tenant or parent resource.

### Custom Authorization

If the app uses custom roles or permission helpers, verify:

- Default deny behavior.
- Centralized helpers instead of scattered `admin?` checks.
- Tenant and ownership predicates appear in data-loading queries, not only after loading records.
- All mutation paths share the same authorization rule.
- Role changes, invitations, and membership updates cannot grant more privilege than the actor has.
- Tests cover the custom rules.

## Step 5: Verify Controller Access Matches Expectations

Create an access matrix from routes, controllers, and policies.

```markdown
| Route | Controller#Action | Public? | Required Role | Ownership/Tenant Rule | Policy/Ability | Expected Unauthorized | Expected Wrong Tenant | Expected Allowed |
|-------|-------------------|---------|---------------|------------------------|----------------|-----------------------|-----------------------|------------------|
```

For every sensitive action, compare expected behavior with implementation:

- `index`: Does it scope records to the current user/account/tenant?
- `show`: Does it load through an authorized scope before rendering?
- `new/create`: Can submitted foreign keys attach records to another tenant?
- `edit/update`: Are both the target record and any submitted related IDs authorized?
- `destroy`: Does it enforce ownership, role, state, and tenant boundaries?
- Custom actions: `archive`, `restore`, `publish`, `approve`, `invite`, `export`, `impersonate`, `refund`, `sync`, `resend`, `transfer`.

Flag these patterns:

- `Model.find(params[:id])` before tenant scoping.
- `find_by(id: params[:id])` followed by manual checks that leak existence.
- Strong params permit `*_id`, `role`, `admin`, or permission fields without verifying the referenced record and privilege change are allowed.
- `before_action :authenticate_user!` exists but no authorization runs.
- Authorization runs after rendering, redirecting, or side effects.
- View-level checks hide links but controller actions remain callable.
- Admin checks use `current_user.admin?` without tenant or environment constraints.
- API controllers skip CSRF without token, origin, or signature protections.

## Step 6: Test the Access Model

Prefer request specs or system specs that exercise real routes. Test roles and tenants, not only happy paths.

Minimum cases for sensitive controllers:

- Anonymous user.
- Authenticated user with no role.
- User from another tenant.
- User with read-only role.
- Owner/member with expected role.
- Admin or support user, if applicable.
- Expired or revoked API token.
- Wrong-scope API token.

Example RSpec shape:

```ruby
RSpec.describe ProjectsController, type: :request do
  describe "PATCH /projects/:id" do
    it "rejects anonymous users"
    it "rejects users from another account"
    it "rejects members without edit permission"
    it "allows account owners"
    it "does not allow changing account_id through params"
  end
end
```

For policies, add direct policy specs when useful:

```ruby
RSpec.describe ProjectPolicy do
  subject(:policy) { described_class.new(user, project) }

  it "denies cross-account access"
  it "allows owners to update"
  it "denies viewers from destroying"
end
```

For APIs, assert status and response shape:

- `401` for unauthenticated.
- `403` or `404` for authenticated but unauthorized. Use one convention and avoid record enumeration leaks.
- Generic login, activation, and password reset responses that avoid user enumeration.
- No sensitive fields in error responses.
- No state change after unauthorized requests.

## Step 7: Review High-Risk Rails Auth Areas

Focus extra attention on:

- Multi-tenant apps and account switching.
- Select boxes, radio buttons, and checkboxes populated from unscoped associations instead of `policy_scope` / authorized scopes.
- Invitations and membership management.
- Admin namespaces and mounted engines.
- Separate admin credentials, admin subdomain isolation, source IP allowlists, or VPN controls where the risk warrants them.
- Admin 2FA/passkey enforcement and recovery-code handling.
- Support impersonation.
- Billing, refunds, plan changes, and provider IDs.
- Exports, reports, search, and bulk APIs.
- File uploads and ActiveStorage direct uploads.
- Webhooks that map external IDs to local records.
- Background jobs triggered by user input.
- GraphQL mutations and field-level access.
- ActionCable subscriptions and broadcasts.

## Output Format

```markdown
# Rails Authentication and Authorization Audit
## Project
## Auth Stack
## Date

### Access Model Summary
| Actor/Role | Scope | Expected Capabilities |
|------------|-------|-----------------------|

### Route Access Matrix
| Route | Controller#Action | Expected Access | Implementation | Verified? | Notes |
|-------|-------------------|-----------------|----------------|-----------|-------|

### Policy Coverage
| Resource | Framework | Policy/Ability | Scope Rule | Missing Actions | Notes |
|----------|-----------|----------------|------------|-----------------|-------|

### Findings
#### [SEVERITY] [Title]
**File:** `path/to/file.rb:42`
**Category:** Authentication | Authorization | Policy Coverage | Tenant Isolation | IDOR | Test Gap
**Affected Route/Action:** `[verb] /path -> controller#action`
**Expected Access:** [who should access it]
**Actual Behavior:** [what code/tests show]
**Evidence:** [code, route output, spec, request, or console check]
**Remediation:** [specific controller/policy/test change]
**Verification:** [request spec, policy spec, or manual command]
**Disposition:** Fixed | Deferred | Accepted Risk

### Test Plan
1. [Highest-risk missing test]
2. [Next]

### Prioritized Remediation
1. [Critical auth bypass or cross-tenant access]
2. [High missing authorization on mutations]
3. [Medium policy/test coverage gaps]
4. [Low hardening]
```

## Boundaries

- Audit only applications and code the user provides or authorizes.
- Provide fixes and tests, not unauthorized bypass instructions.
- Treat missing tests as a risk signal, not proof of a vulnerability.
- Mark low-confidence findings as potential until verified.
- Refuse requests to weaken access controls, hide authorization gaps, or access data outside scope.

## References

- Rails Security Guide
- OWASP Ruby on Rails Cheat Sheet
- Saeloun Rails Security Best Practices guide
- Pundit documentation
- Action Policy documentation
- CanCanCan documentation
- Devise documentation
- OWASP Access Control Cheat Sheet
- OWASP Authorization Cheat Sheet
