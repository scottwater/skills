---
name: gpt-image-prompts
disable-model-invocation: true
description: Generate professional prompts for OpenAI GPT Image models, especially gpt-image-2. Use when the user wants a prompt for text-to-image generation, image edits, reference-image compositing, photorealistic scenes, ads, logos, infographics, UI mockups, slides, product images, or text-heavy visuals. Transforms vague visual ideas into structured, GPT Image-optimized creative briefs with recommended API settings.
---

# GPT Image Prompt Generator

Generate prompts for OpenAI GPT Image models, with `gpt-image-2` as the default target. Treat the model like a production designer who follows a clear creative brief: define the goal, visual deliverable, subject, composition, constraints, and exact text.

Primary reference: OpenAI's GPT Image Generation Models Prompting Guide: <https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide>

## Default Output When This Skill Is Used

Unless the user asks for another format, return:

1. **Ready-to-use prompt** in a fenced code block.
2. **Recommended API settings**: `model`, `size`, `quality`, `background`, `output_format`, and notes for `n` or edit inputs if relevant.
3. **Optional refinement prompts**: one or two short follow-up edits that improve a likely first pass.

If critical details are missing, ask only the minimum clarifying questions needed. Otherwise, make tasteful assumptions and state them briefly.

## Model Defaults and Constraints

- **Default model:** `gpt-image-2`.
- **Quality:** use `low` for fast drafts, thumbnails, and broad exploration; use `medium` for most production prompts; use `high` for dense text, small labels, infographics, slide/chart outputs, close-up portraits, identity-sensitive edits, and final assets.
- **Size:** use a concrete size when the output format is known; otherwise use `auto`.
  - Common sizes: `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `3840x2160`, `2160x3840`.
  - `gpt-image-2` size constraints: both edges multiples of 16px; max edge ≤ 3840px; long:short ratio ≤ 3:1; total pixels from 655,360 to 8,294,400.
  - Outputs above `2560x1440` are more variable/experimental; prefer 2K or below for reliability unless the user needs 4K.
- **Background:** `gpt-image-2` does **not** support transparent backgrounds. Use `background: "opaque"` for product extraction and plain-background assets; use downstream background removal if transparency is required.
- **Input fidelity:** omit `input_fidelity` for `gpt-image-2`; it processes inputs at high fidelity by default.
- **Output format:** default `png`; choose `jpeg` for lower latency/photo workflows; choose `webp` for compressed web assets.
- **Variations:** use `n` when the user wants multiple directions, logos, thumbnails, or ad concepts.

## Golden Rules

1. **Write a creative brief, not tag soup.** Natural language and labeled sections are better than keyword piles.
2. **Lead with purpose.** Include what the asset is for: product ad, editorial hero image, UI mockup, classroom handout, pitch-deck slide, marketplace listing, etc.
3. **Use a stable prompt order.** Background/scene → subject → details → composition → style/medium → constraints → exact text.
4. **Name the visual medium explicitly.** Use phrases like `photorealistic`, `vector-like logo`, `flat scientific diagram`, `mobile app UI mockup`, `pitch-deck slide`, or `comic strip`.
5. **Specify composition.** Framing, viewpoint, subject placement, negative space, camera angle, lighting, mood, and color palette all matter.
6. **Preserve invariants in edits.** Use “change only X; keep everything else the same,” then list the preserved identity/layout/geometry/typography/lighting elements.
7. **Quote exact text.** Put in-image copy in quotes and specify typography, placement, contrast, and “no extra text.” For hard spellings, spell words letter by letter.
8. **Iterate surgically.** For an 80%+ good result, write narrow follow-up prompts instead of re-rolling: “make the lighting warmer,” “remove the extra label,” “restore the original background.”

## Prompt Structure Template

Use labeled sections for complex or production prompts:

```text
Create [DELIVERABLE] for [PURPOSE/AUDIENCE].

Scene / background:
[Environment, era, mood, context, world details]

Subject:
[Main subject with concrete attributes, materials, identity cues, pose/action]

Composition:
[Framing, viewpoint, camera angle, placement, negative space, layout hierarchy]

Style / medium:
[Photorealistic / editorial / vector / 3D render / UI / diagram / comic, color palette, lighting]

Text, if any:
Render exactly: "..."
[Typography, size, placement, contrast]

Constraints:
[No extra text, no watermark, no unrelated logos, preserve X, avoid Y]
```

For simple requests, a polished paragraph is enough. For production work, labeled sections are easier to debug and reuse.

## Capability-Specific Patterns

### Photorealistic Images

Use the word **photorealistic** directly. Prompt as if a real photo is being captured in the moment, with natural imperfections.

Include:
- camera framing: wide shot, medium close-up, top-down, eye-level, low-angle
- lighting: soft coastal daylight, golden hour, overcast diffuse light, practical indoor lighting
- real textures: pores, wrinkles, fabric wear, scratches, dust, condensation, fingerprints
- anti-polish constraints: no glamorization, no heavy retouching, no plastic skin, no stock-photo look

Avoid relying on exact lens specs for physics; use them mainly for high-level look and composition.

### People, Pose, and Action

State body framing, scale, gaze, and interactions:
- “full body visible, feet included”
- “looking down at the open book, not at the camera”
- “hands naturally gripping the handlebars”
- “child-sized relative to the table”
- “preserve the person’s exact face, body shape, hairstyle, expression, and pose”

### Text, Typography, and Infographics

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

### Ads and Marketing Creative

Write like a creative director:
- brand name, positioning, target audience, channel, and cultural vibe
- scene/concept, emotional promise, and composition
- exact copy/tagline if needed
- constraints around trademarks, watermarks, extra text, and brand safety

### Logos and Brand Marks

Ask for original, non-infringing, simple marks:
- clean vector-like shapes
- strong silhouette and balanced negative space
- flat design, minimal strokes, no gradients unless essential
- centered on a plain opaque background with generous padding
- readable at small and large sizes

Use `n: 4` or more for logo exploration.

### UI Mockups and Product Screens

Describe the product as if it already exists. Focus on usability and hierarchy, not concept art.

Include:
- device/frame or canvas
- core screens/sections
- typography, spacing, color system
- realistic content, not lorem ipsum if possible
- practical constraints: real app UI, clear hierarchy, minimal decoration, no impossible controls

### Slides, Charts, and Productivity Visuals

Prompt as an artifact spec:
- title and canvas orientation
- exact numbers, labels, legends, and footnotes
- chart type and hierarchy
- design language: crisp startup deck, editorial report, classroom slide, internal strategy doc
- constraints: readable text, polished spacing, no stock photography, no decorative clutter

Use `1536x864` or another 16:9 size for slides; use `quality: "high"` for charts/small text.

### Product Images and Marketplace Assets

For extraction/mockups:
```text
Extract the product from the input image and place it on a plain white opaque background.
Preserve product geometry and label legibility exactly.
Centered product, crisp silhouette, no halos or fringing.
Add only subtle realistic contact shadow. Do not restyle the product.
```

For product photography, specify surface, lighting, scale, camera angle, and material detail.

### Image Editing

Use explicit edit boundaries:
```text
Change only [target change]. Keep everything else exactly the same: identity, background, camera angle, framing, lighting, colors, saturation, contrast, typography, arrows, labels, and surrounding objects. Do not add text, logos, watermarks, or new elements.
```

For translation/localization:
```text
Translate only the text to [language]. Preserve layout, typography style, placement, spacing, hierarchy, icons, logos, imagery, and colors. Do not add extra words or change any non-text element.
```

For virtual try-on:
```text
Replace only the clothing using the reference garment images. Preserve the person’s exact face, identity, skin tone, body shape, pose, hairstyle, expression, and proportions. Fit the garments naturally with realistic drape, folds, occlusion, lighting, and shadows. Do not change background, camera angle, framing, or image quality.
```

### Multi-Image Reference and Compositing

Always identify inputs by index and role:

```text
Image 1: base product photo.
Image 2: brand style reference.
Image 3: background environment.

Create a new image using the product from Image 1, the color palette and lighting language from Image 2, and the environment from Image 3. Preserve the product geometry and label exactly. Place the product centered in the foreground, scaled realistically, with matching shadows.
```

Be explicit about what moves where and what stays unchanged.

### Comics, Storyboards, and Multi-Panel Layouts

Define one visual beat per panel:
- number of panels and layout
- concrete action per panel
- consistent character identity and attire
- readable emotional arc
- no extra captions unless specified

## Reusable Prompt Patterns

### Production Photorealism

```text
Create a photorealistic candid photograph of [subject] in [setting].
[Subject] is [action/pose], with [specific natural details and imperfections].
Composition: [framing], [viewpoint], [camera distance], [what is visible].
Lighting: [natural/practical lighting], [mood], [color balance].
The image should feel honest and unstaged, with real textures in [skin/fabric/materials/environment].
Avoid a stock-photo look, heavy retouching, plastic surfaces, extra text, logos, or watermarks.
```

### Clean Infographic

```text
Create a clean [vertical/horizontal] infographic titled "[TITLE]" for [audience].
Goal: explain [concept] clearly at a glance.
Include these sections: [section list].
Required labels: [labels/data].
Visual style: [flat/vector/editorial/technical], white space, consistent icons, clear arrows, readable sans-serif text.
Constraints: no tiny text, no extra sections, no decorative clutter, no watermark.
```

### Surgical Edit

```text
Edit the input image to [specific change].
Change only [target area/object].
Preserve exactly: [identity/product geometry/layout/background/camera angle/framing/lighting/colors/text].
Match the original image’s perspective, shadows, grain, color temperature, and quality.
Do not add new elements, extra text, logos, or watermarks.
```

### Ad With Exact Copy

```text
Create a polished [channel] ad for [brand], a [positioning] brand for [audience].
Concept: [scene/story/emotional hook].
Composition: [subject placement, product placement, negative space, layout].
Style: [photography/design direction, palette, lighting, cultural cues].
Text: render exactly "[COPY]" [placement/type style].
Constraints: tagline appears exactly once, no extra text, no unrelated logos, no watermark.
```

## Prompt Transformation Examples

❌ **Vague:** “make a coffee machine infographic”

✅ **GPT Image prompt:**
```text
Create a detailed vertical infographic titled "How an Automatic Coffee Machine Works" for curious home coffee users.
Show the internal flow from bean hopper to grinder, dosing chamber, water tank, pump, boiler/thermoblock, brew group, pressure extraction, spout, drip tray, and used puck container.
Use a clean technical editorial style with cutaway diagrams, arrows, numbered steps, and short readable labels.
White background, muted grays with warm coffee-brown accents, clear hierarchy, generous spacing.
Avoid tiny text, decorative clutter, brand logos, or inaccurate extra mechanisms.
```
Settings: `model="gpt-image-2"`, `size="1024x1536"`, `quality="high"`.

❌ **Vague:** “realistic old sailor”

✅ **GPT Image prompt:**
```text
Create a photorealistic candid photograph of an elderly sailor standing on a small fishing boat near the coast.
He is calmly adjusting a net while a weathered dog sits nearby on the deck. His skin has visible wrinkles, pores, sun texture, and faded sailor tattoos. Clothing is worn, practical, salt-stained, and wind-creased.
Composition: medium close-up at eye level, natural body posture, boat details visible around him.
Lighting: soft coastal daylight, natural color balance, subtle film grain, shallow depth of field.
The image should feel honest and unposed, with real skin, fabric, rope, wood, and metal textures.
No glamorization, no heavy retouching, no stock-photo look, no text, no watermark.
```
Settings: `model="gpt-image-2"`, `size="1024x1536"`, `quality="medium"`.

❌ **Vague:** “change this ad to Spanish”

✅ **GPT Image edit prompt:**
```text
Translate only the visible ad text into Spanish.
Preserve every non-text element exactly: layout, typography style, text placement, spacing, hierarchy, logo, product image, icons, background, colors, shadows, and image quality.
Do not add extra words. Do not recompose the ad. Do not change the product, people, logos, or imagery.
```
Settings: `model="gpt-image-2"`, `quality="high"` for text fidelity.
