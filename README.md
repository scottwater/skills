# Skills

A collection of agent skills for use with coding agents.

## Install

```bash
npx skills add scottwater/skills
```

See the [skills CLI](https://github.com/vercel-labs/skills) for more options and supported agents.

## Available Skills

### Gemini Image Generation

> [!NOTE]
> This skill is heavily based on the similarly named skill in the excellent
> [compounding engineering plugin](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering/skills/gemini-imagegen). The only major difference is that this
> skill uses `uv`, which makes it easier to operate.

`gemini-imagegen` — Generate and edit images using the Gemini API (Nano Banana Pro), supporting text-to-image, image editing, multi-turn refinement, and composition from multiple reference images.


### Nano Banana Pro Prompts

`nano-banana-prompts` — Generate professional prompts for Nano Banana Pro image generation, transforming vague requests into detailed, effective prompts following its "thinking model" best practices.

### GPT Image Prompts

`gpt-image-prompts` — Generate professional prompts for OpenAI GPT Image models, especially `gpt-image-2`, transforming vague visual requests into structured creative briefs with recommended API settings for generation, edits, compositing, text-heavy visuals, ads, logos, UI mockups, slides, and product images.

### Rails Cybersecurity

A grouped set of Rails-focused security validation skills. These skills favor concrete checks, file paths, commands, test gaps, and remediation over generic security explanation.

| Skill | Description |
| --- | --- |
| `rails-cybersecurity/rails-security-core` | Run routine codebase or diff review across auth/authz, OWASP appsec, dependencies, and prompt-injection checks. |
| `rails-cybersecurity/rails-security-broad` | Run core Rails security review plus repository-only cloud, platform, IaC, deployment, and configuration review. |
| `rails-cybersecurity/rails-security-validation` | Run validation-focused Rails security review across major security lenses. |
| `rails-cybersecurity/rails-auth-audit` | Review authentication, authorization, policies, roles, tenants, sessions, tokens, and controller access. |
| `rails-cybersecurity/owasp-audit` | Audit Rails, Ruby, and JavaScript source against OWASP-style application security risks. |
| `rails-cybersecurity/dependency-audit` | Review Ruby, Rails, gem, JavaScript, lockfile, CI, and supply-chain security posture. |
| `rails-cybersecurity/prompt-injection` | Review AI, LLM, RAG, agent, MCP, automation, prompt, tool-use, and output-handling security. |
| `rails-cybersecurity/cloud-audit` | Review repository evidence for cloud, platform, deployment, infrastructure, and operational security configuration. |
| `rails-cybersecurity/recon` | Enumerate web application attack surface and reconnaissance targets when authorized scope is available. |
| `rails-cybersecurity/osint-recon` | Gather and correlate open source intelligence for authorized targets. |
| `rails-cybersecurity/incident-triage` | Triage security incidents using structured evidence collection and prioritization. |
| `rails-cybersecurity/disk-forensics` | Analyze disk images, recover evidence, and build forensic timelines. |

### Code Quorum

`code-quorum` runs a read-only review through independent lenses, verifies material findings, and returns one prioritized report. It reviews pending changes by default and accepts a PR, branch, revision range, commit, file set, diff, or supplied artifact.

| Mode | Reviewers |
| --- | --- |
| `quick` | General reviewer and silent-failure hunter |
| `default` | Adversarial reviewer, general reviewer, silent-failure hunter, and skeptical engineer |
| `full` | Default reviewers plus simplification reviewer |

Request a mode or named combination, such as `Run a quick code quorum` or `Use the skeptical engineer and silent-failure hunter from code-quorum`.

### Inertia Docs

> [!IMPORTANT]
> I do not recommend using these skills. Using skills for non-procedural work has
> been a misstep, and it is something I am backing away from. I will likely remove
> the Inertia.js skills in the near future.

A comprehensive set of skills for working with Inertia.js (Rails + React). Covers setup, conventions, and common patterns.

| Skill | Description |
| --- | --- |
| `inertia-reference` | Overview and project conventions for Inertia Rails + React. |
| `inertia-rails-setup` | Set up and configure inertia_rails + React/Vite. |
| `inertia-rendering-props` | Render Inertia responses, shared data, and lazy or deferred props. |
| `inertia-forms-validation` | Inertia useForm patterns, custom Form helper, and validation errors. |
| `inertia-navigation` | Links, navigation, partial reloads, scroll, and cache control. |
| `inertia-layouts` | Persistent and nested layout patterns for Inertia pages. |
| `inertia-ssr` | Server-side rendering setup for Inertia Rails + React. |
| `inertia-auth` | Authentication and authorization patterns with Inertia. |
| `inertia-testing` | RSpec request testing for Inertia responses. |
| `inertia-pitfalls` | Common Inertia Rails gotchas and fixes. |

## License

[MIT](LICENSE)
