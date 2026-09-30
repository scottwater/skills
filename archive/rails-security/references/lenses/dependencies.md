# Dependencies Lens

Known-vulnerable and risky components, triaged with scanners that run in development.

## Run

Run what applies; report a missing tool once, as a gap.

```bash
bundle exec brakeman -q
bundle audit check --update
bundle outdated --strict | head -30
bin/importmap audit 2>/dev/null            # import maps
npm audit --omit=dev --json 2>/dev/null || yarn npm audit 2>/dev/null || pnpm audit --json 2>/dev/null
ruby -v && (bin/rails -v 2>/dev/null || bundle exec rails -v)
```

## Search

- Verify every advisory against the installed version in `Gemfile.lock` or the JavaScript lockfile — never against a loose constraint — and classify exposure: runtime, build-time, dev/test-only, or transitive with the vulnerable path unreached.
- Ruby and Rails versions outside their security-support window.
- Brakeman findings and the ignore file: every ignored warning needs a reason that is still true; re-raise the ones that aren't.
- Unpinned git gems, branch-based dependencies, and mixed gem sources without source blocks.
- Unmaintained gems sitting in auth, crypto, file parsing, or payment paths.

## Evidence bar

Package, installed version, advisory/CVE, exposure class, and fix version or compensating control. Clean scanner output is neither a finding nor proof of a clean app.

## Exclude

Docker images, CI workflows, IaC, host packages, and deployment platforms.
