# GPT Image Capability Patterns

Apply the sections that match the deliverable. Each template is fill-in-ready; combine it with the prompt structure template in `SKILL.md`.

## Photorealistic images

Use the word **photorealistic** directly. Prompt as if a real photo is being captured in the moment, with natural imperfections.

Include:

- camera framing: wide shot, medium close-up, top-down, eye-level, low-angle
- lighting: soft coastal daylight, golden hour, overcast diffuse light, practical indoor lighting
- real textures: pores, wrinkles, fabric wear, scratches, dust, condensation, fingerprints
- anti-polish constraints: no glamorization, no heavy retouching, no plastic skin, no stock-photo look

Avoid relying on exact lens specs for physics; use them mainly for high-level look and composition.

```text
Create a photorealistic candid photograph of [subject] in [setting].
[Subject] is [action/pose], with [specific natural details and imperfections].
Composition: [framing], [viewpoint], [camera distance], [what is visible].
Lighting: [natural/practical lighting], [mood], [color balance].
The image should feel honest and unstaged, with real textures in [skin/fabric/materials/environment].
Avoid a stock-photo look, heavy retouching, plastic surfaces, extra text, logos, or watermarks.
```

## People, pose, and action

State body framing, scale, gaze, and interactions:

- “full body visible, feet included”
- “looking down at the open book, not at the camera”
- “hands naturally gripping the handlebars”
- “child-sized relative to the table”
- “preserve the person’s exact face, body shape, hairstyle, expression, and pose”

## Text, typography, and infographics

For any text-heavy output, recommend `quality: "high"`.

Prompt like an instructional/design brief:

- Define the audience and learning/business goal.
- List required sections, labels, data, and exact text.
- Specify visual hierarchy, readable typography, arrows/legends/spacing.
- Say “avoid tiny text” and “no extra words.”

For literal text:

```text
Render the headline exactly once: "Yours to Create."
Use bold clean sans-serif typography, high contrast, centered near the bottom.
No other text, no watermark, no unrelated logos.
```

For infographics:

```text
Create a clean [vertical/horizontal] infographic titled "[TITLE]" for [audience].
Goal: explain [concept] clearly at a glance.
Include these sections: [section list].
Required labels: [labels/data].
Visual style: [flat/vector/editorial/technical], white space, consistent icons, clear arrows, readable sans-serif text.
Constraints: no tiny text, no extra sections, no decorative clutter, no watermark.
```

## Ads and marketing creative

Write like a creative director: brand name, positioning, target audience, channel, cultural vibe; scene/concept, emotional promise, composition; exact copy/tagline if needed; constraints around trademarks, watermarks, extra text, and brand safety.

```text
Create a polished [channel] ad for [brand], a [positioning] brand for [audience].
Concept: [scene/story/emotional hook].
Composition: [subject placement, product placement, negative space, layout].
Style: [photography/design direction, palette, lighting, cultural cues].
Text: render exactly "[COPY]" [placement/type style].
Constraints: tagline appears exactly once, no extra text, no unrelated logos, no watermark.
```

## Logos and brand marks

Ask for original, non-infringing, simple marks:

- clean vector-like shapes
- strong silhouette and balanced negative space
- flat design, minimal strokes, no gradients unless essential
- centered on a plain opaque background with generous padding
- readable at small and large sizes

Use `n: 4` or more for logo exploration.

## UI mockups and product screens

Describe the product as if it already exists. Focus on usability and hierarchy, not concept art.

Include:

- device/frame or canvas
- core screens/sections
- typography, spacing, color system
- realistic content, not lorem ipsum if possible
- practical constraints: real app UI, clear hierarchy, minimal decoration, no impossible controls

## Slides, charts, and productivity visuals

Prompt as an artifact spec:

- title and canvas orientation
- exact numbers, labels, legends, and footnotes
- chart type and hierarchy
- design language: crisp startup deck, editorial report, classroom slide, internal strategy doc
- constraints: readable text, polished spacing, no stock photography, no decorative clutter

Use `1536x864` or another 16:9 size for slides; use `quality: "high"` for charts/small text.

## Product images and marketplace assets

For extraction/mockups:

```text
Extract the product from the input image and place it on a plain white opaque background.
Preserve product geometry and label legibility exactly.
Centered product, crisp silhouette, no halos or fringing.
Add only subtle realistic contact shadow. Do not restyle the product.
```

For product photography, specify surface, lighting, scale, camera angle, and material detail.

## Image editing and localization

Use explicit edit boundaries:

```text
Edit the input image to [specific change].
Change only [target area/object].
Preserve exactly: [identity/product geometry/layout/background/camera angle/framing/lighting/colors/text].
Match the original image’s perspective, shadows, grain, color temperature, and quality.
Do not add new elements, extra text, logos, or watermarks.
```

For translation/localization:

```text
Translate only the text to [language]. Preserve layout, typography style, placement, spacing, hierarchy, icons, logos, imagery, and colors. Do not add extra words or change any non-text element.
```

For virtual try-on:

```text
Replace only the clothing using the reference garment images. Preserve the person’s exact face, identity, skin tone, body shape, pose, hairstyle, expression, and proportions. Fit the garments naturally with realistic drape, folds, occlusion, lighting, and shadows. Do not change background, camera angle, framing, or image quality.
```

## Multi-image reference and compositing

Always identify inputs by index and role, and be explicit about what moves where and what stays unchanged:

```text
Image 1: base product photo.
Image 2: brand style reference.
Image 3: background environment.

Create a new image using the product from Image 1, the color palette and lighting language from Image 2, and the environment from Image 3. Preserve the product geometry and label exactly. Place the product centered in the foreground, scaled realistically, with matching shadows.
```

## Comics, storyboards, and multi-panel layouts

Define one visual beat per panel:

- number of panels and layout
- concrete action per panel
- consistent character identity and attire
- readable emotional arc
- no extra captions unless specified
