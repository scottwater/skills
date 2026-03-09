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
