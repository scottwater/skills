---
name: github-social
disable-model-invocation: true
description: Generate a 1280x640 GitHub repository social preview (Open Graph) image and link it at the top of the README.
---

# GitHub Social Preview

Create a 1280x640 PNG social preview for a GitHub repository, using `repository-open-graph-template.png` (in this skill's folder) as the safe-area reference.

## Generation route

Use the host's built-in image-generation tool (`image_gen` in Codex), with its existing account authentication. This skill is built-in-only: never request, inspect, or configure `OPENAI_API_KEY`; never offer or run an API/CLI image-generation fallback. If consulting the general `imagegen` skill, use only its built-in workflow and prompting guidance; its fallback branch does not apply here.

Discover the tool in the current session, including deferred-tool discovery when available. A listed skill, image-viewing tool, or image-capable chat model does not establish image-generation availability. If the tool is present, call it using its actual schema; missing model/size/path controls are not a reason to change routes.

Let the built-in tool select its default image model. OpenAI's [built-in image-generation docs](https://learn.chatgpt.com/docs/image-generation) currently name `gpt-image-2`; the separate [API docs](https://developers.openai.com/api/docs/guides/tools-image-generation) name `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare`. API model availability does not imply a built-in model selector. Honor an explicitly requested model only when the exposed tool supports it; otherwise explain that limit. Never change the coding/chat model to an image-model ID or claim an unreported backend model.

If discovery finds no generation tool, report that this session does not expose built-in image generation and return the completed prompt for use in a session that does. If a call fails, report the actual error; retry only when the error indicates a transient failure or a correctable argument. Keep the existing preview and README intact until a valid image exists.

For T3/SDK sessions, diagnose the host/provider boundary before blaming the prompt: check the Codex binary/version the host launches, its effective provider/authentication, and image-generation feature/tool exposure. A local CLI feature flag or ChatGPT login alone does not prove the hosted session has the tool. Custom providers may omit built-in capabilities. Recommend a session exposing the built-in tool; do not change global provider configuration as part of image creation.

## Workflow

1. Gather repo signal from the request and local files: repo name, owner/org, README tagline, logo or mark, brand colors, primary language, and audience. Done when every bracket in the prompt template can be filled.
2. Draft the prompt from the template below and follow the generation route above. Load `repository-open-graph-template.png` with the image-viewing tool when needed to make it available as a reference; use the generation tool's supported reference mechanism, or rely on the written safe-area constraint.
3. Normalize the generated artifact to exactly 1280x640 opaque PNG with local image processing if needed, preserving proportions and the safe area. Inspect the final image at full size and at roughly 320x160. Regenerate or edit until every check passes: repo name spelled correctly and readable at thumbnail size, all critical content inside the safe area, no guide lines, template copy, watermarks, or unintended logos, and the visual matches the repository's actual purpose and tone.
4. Save to `assets/github-social-preview.png`, creating `assets/` if needed, unless the user names another path or that name collides with a file they want preserved.
5. Link the image at the very top of `README.md` with a relative Markdown image link — before any badges or logo — unless the user opts out or asks for different placement. Repoint or replace an existing preview block instead of adding a second. If `README.md` does not exist, ask before creating one.

```markdown
![Repository social preview](assets/github-social-preview.png)
```

## Specs

- Canvas: exactly 1280x640, opaque PNG — the size GitHub's Settings > Social preview uploader expects.
- Safe area: all critical text, logos, faces, and visual focus inside the template's inner rectangle (about 80px from each edge); nonessential background texture may bleed past it.
- Text: large, sparse, high-contrast — repo name plus at most one short descriptor.
- Composition: one strong concept, not a collage — a project mark beside the repo name and tagline, or an abstract product/code motif tied to the repository. Palette drawn from the repo's brand; generic purple-blue gradients only when they are the brand.
- Assets: use real project assets when provided; otherwise create an original simple mark. Third-party logos and GitHub's own mark stay out unless the user explicitly requests GitHub branding.

## Prompt template

```text
Create a GitHub repository social preview image for [REPO_NAME].

Canvas and purpose:
1280x640 PNG, opaque background, designed for GitHub repository Settings > Social preview / Open Graph sharing.

Repository signal:
[OWNER_OR_ORG], [SHORT_DESCRIPTION], [LANGUAGE_OR_DOMAIN], [BRAND_COLORS_OR_VISUAL_MOOD].

Composition:
Keep all important details inside an 80px safe margin on every edge, matching the safe-area of the GitHub repository-open-graph-template reference. Use a bold, readable layout with one primary focal element and generous spacing. The image must still read clearly when reduced to 320x160.

Text:
Render exactly: "[REPO_NAME]"
Optional subtitle, if useful: "[TAGLINE]"
Use large, crisp, high-contrast typography. No extra words.

Style:
[DISTINCTIVE_STYLE_DIRECTION]. Polished production design, not a screenshot of GitHub settings, not a generic stock banner.

Constraints:
Do not include red guide lines, template labels, watermarks, tiny text, unrelated logos, or GitHub branding unless explicitly requested. Keep edges crop-safe.
```

Request a high-quality, opaque 1280x640 PNG in the prompt. Pass structured options only when the built-in tool exposes them. Copy the selected generated artifact into the repository before linking it from the README.
