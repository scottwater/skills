---
name: github-social
description: Generate polished GitHub repository social preview / Open Graph images. Use when the user asks for a GitHub social preview, repo card, repository Open Graph image, GitHub preview image, or an image sized for the repository social preview uploader. Uses the repository-open-graph-template.png safe-area template, targets gpt-image-2, and should not require an OpenAI API key.
---

# GitHub Social Preview

Create a 1280x640 PNG social preview image for a GitHub repository, using `repository-open-graph-template.png` as the safe-area reference.

## Workflow

1. Gather repo signal from the user request and local files when available: repo name, owner/org, README tagline, logo/mark, brand colors, domain, primary language, and intended audience.
2. If the `gpt-image-prompts` skill is available, load it and use it to draft the GPT Image prompt. Keep this skill's GitHub-specific constraints authoritative.
3. Generate with the built-in image generation capability targeting `gpt-image-2`. Do not ask for an API key, call the OpenAI REST API, or require `OPENAI_API_KEY`.
4. Use `repository-open-graph-template.png` as a reference image when the image tool supports reference inputs. Otherwise, manually apply the constraints below.
5. Inspect the result at full size and thumbnail size. Regenerate or edit if text is misspelled, cramped, low contrast, outside the safe area, or if guide lines/template text appear.

If the available image tool does not expose a model selector, still write the prompt and settings for `gpt-image-2`; use the local tool without asking the user for credentials.

## Required Specs

- Canvas: exactly 1280x640, PNG, opaque background.
- GitHub upload target: repository Settings > Social preview.
- Safe area: keep all critical text, logos, faces, product UI, and visual focus inside the inner rectangle shown by `repository-open-graph-template.png` (about 80px from each edge on the 1280x640 template).
- Crop tolerance: allow nonessential background texture outside the safe area.
- Text: large, sparse, high-contrast. Prefer repo name plus one short descriptor. Avoid tiny labels.
- Final image must not contain the template's red guide lines, "Repo Card Template" copy, or GitHub logo unless the user explicitly requests GitHub branding.

## Composition Guidance

Prefer one strong concept over a collage:

- Left or centered project mark, right/center repo name and tagline.
- Abstract product metaphor, code/tooling motif, or UI fragment tied to the repository.
- Distinct palette from the repo/brand; avoid generic purple-blue gradients unless brand-specific.
- Readable at small social-card sizes; test by viewing around 320x160.

Use real project assets if provided. If no logo exists, create an original simple mark; do not invent third-party logos or copy GitHub's mark from the template.

## Prompt Template

Use or adapt this with the `gpt-image-prompts` skill:

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

Recommended settings:

```yaml
model: gpt-image-2
size: 1280x640
quality: high
background: opaque
output_format: png
```

## QA Checklist

- Dimensions are 1280x640.
- All critical content sits inside the template safe area.
- Repo name is spelled correctly and readable at thumbnail size.
- No template artifacts, guide lines, watermarks, or unintended logos.
- Visual matches the repository's actual purpose and tone.
