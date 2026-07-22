# Access Control Lens

Authentication, authorization, tenant isolation, sessions, CSRF, and webhook identity in Rails code.

## Map

```bash
bin/rails routes 2>/dev/null || bundle exec rails routes
grep -n "devise\|rodauth\|sorcery\|omniauth\|doorkeeper\|pundit\|action_policy\|cancancan\|bcrypt" Gemfile.lock
grep -rn "mount " config/routes.rb config/routes 2>/dev/null
grep -rn "before_action\|skip_before_action\|authenticate_\|authorize\|policy_scope\|authorized_scope\|accessible_by\|skip_authorization\|skip_policy_scope\|current_user\|current_account" app/
grep -rn "\.find(params\|find_by(id: params\|params\[:.*_id\]\|permit(.*_id\|permit(.*role\|permit(.*admin" app/
```

## Search

- Unscoped lookups: `Model.find(params[:id])` or `find_by(id: params[:id])` without tenant or policy scoping. The safe shape is `current_account.projects.find(params[:id])` or a policy scope.
- Permitted privilege and foreign-key params — `account_id`, `user_id`, `role`, `admin`, `plan_id` — reaching create/update; strong params and `params.expect` do not replace authorization.
- Controllers, API endpoints, GraphQL resolvers, jobs, mailers, channels, and exports that read or mutate tenant data without a policy check; custom actions (`archive`, `publish`, `approve`, `invite`, `export`, `impersonate`, `transfer`) with no matching policy method.
- Mounted engines — Sidekiq::Web, RailsAdmin, ActiveAdmin, Avo, Administrate, Blazer, Flipper, PgHero, GoodJob — unauthenticated, guarded only in production, or guarded by an optional env var that fails open.
- Policy framework coverage: `ApplicationPolicy`/`Ability` defaults to deny; index and collection queries use `policy_scope`/`authorized_scope`/`accessible_by`; `skip_authorization`/`skip_policy_scope` is rare, intentional, and tested; policy scopes cannot return another tenant's records.
- View-only enforcement: links hidden with `can?`/`allowed_to?` while the controller action stays callable; select and checkbox options populated from unscoped associations.
- Authentication mechanics: timing-safe login (`authenticate_by` or equivalent), `reset_session` after login, logout, and privilege elevation; session cookies with `Secure`, `HttpOnly`, and appropriate `SameSite`; idle/absolute expiry matched to sensitivity; sessions storing secrets, balances, or authorization decisions instead of server-side records.
- Tokens: reset, invitation, activation, and magic-link tokens that expire, reject reuse, and reject blank parameters; API tokens with expiry, scoping, and constant-time comparison; generic login/reset responses that never reveal whether an account exists.
- Abuse controls: `rate_limit`, Rack::Attack, or lockout on login, reset, signup, invite, and magic-link endpoints; password, email, and MFA changes requiring the current password or recent re-authentication.
- CSRF: `protect_from_forgery` intact; state-changing routes never on GET; custom fetch/Turbo code sending `X-CSRF-Token`; token-only API controllers may skip cookie CSRF only when cookies never authenticate those paths; remember-me cookies cleared on `InvalidAuthenticityToken`.
- Webhooks: signature validation with `secure_compare`, replay windows, and external-ID → local-record mapping that respects tenant boundaries.
- Sibling paths: when one route enforces ownership, state, or immutability, sweep every sibling route, job, and resolver touching the same model or transition.

## Evidence bar

Named route or action, who gains what access, and the missing check — with `file:lines`. A missing request spec for a denied or wrong-tenant path is a medium test-gap finding, not a vulnerability.

## Exclude

Server and network hardening (VPNs, IP allowlists, TLS termination), infrastructure IAM, and roles the application does not model.
