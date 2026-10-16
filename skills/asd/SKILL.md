---
name: asd
description: Explain a topic in ASD-STE100 Simplified Technical English, or as a diagram, web page, or explainer video.
disable-model-invocation: true
---

# ASD

Explain the topic so a reader understands it fast. Every format uses ASD-STE100 Simplified Technical English: the controlled language written for aerospace maintenance manuals.

Request: $ARGUMENTS

## Pick the format

Take the format the request names. When it names none, use **text**.

| Format | Ask words | Output |
| --- | --- | --- |
| text | default, "strict" | Prose in strict STE |
| soft | "soft", "80%", "lighter" | Prose about 80% of the way to STE |
| diagram | "diagram", "picture", "chart" | A diagram with STE labels and captions |
| html | "HTML", "web page", "interactive" | A self-contained, interactive web page with STE text |
| video | "video", "3b1b", "explainer" | A narrated explainer video with an STE script |

Done when you can name one format and the one topic it explains.

## Write in STE

Apply every rule to all text the reader sees: prose, labels, captions, and narration.

- **Approved words.** Use common words with one meaning each, and keep that meaning ("close" means shut, never "near"). Use the topic's technical names, and keep each name the same through the whole output.
- **Short sentences.** Descriptive sentences have 25 words or fewer; instructions have 20 or fewer. Write one topic in each paragraph and six sentences or fewer in each paragraph. Put the topic sentence first.
- **Active voice.** Name the actor: "The scheduler starts the job."
- **Simple tenses.** Use the present, simple past, and simple future.
- **Verbs for actions.** Write "test the valve", not "do a test of the valve". Use single-word verbs, not phrasal verbs.
- **Short noun clusters.** Use three nouns or fewer in a row; split longer ones with "of" or a relative clause.
- **Complete sentences.** Keep the articles, "that", and other small words that prevent ambiguity.
- **Instructions.** Use the imperative, one action in each sentence, and a numbered list for steps. Put a warning or caution before the step it applies to.
- **Lists.** Use a vertical list for three or more parallel items.

In **soft** format, keep the sentence, voice, and terminology rules, and relax the approved-word rule: use a common word with a second meaning, or a clear phrasal verb, when it reads more naturally.

## Build the output

### text and soft

Give a one-sentence summary first. Then explain with headings and short paragraphs, and give an example when the topic is abstract.

Done when every sentence obeys the STE rules for the format.

### diagram

Pick the diagram type that fits the topic's shape: flowchart for a process, sequence diagram for messages over time, block diagram for structure, state diagram for modes. Render it in Mermaid when the output surface displays Mermaid; otherwise write an SVG file. Add a caption of three STE sentences or fewer.

Done when the diagram renders and every label and caption obeys STE.

### html

Write one self-contained HTML file with inline CSS and JavaScript. Make the reader do something: step through a process, toggle a state, drag a value and see the effect. Use animation where it shows change over time. When the runtime has an HTML preview or render tool, use it to check and show the page; otherwise give the file path.

Done when the page loads with no console errors and all its text obeys STE.

### video

Make a 3Blue1Brown-style explainer: animated visuals that build the idea step by step, synchronized to narration. Ask the user before you install a tool.

1. Write the narration script in STE, split into scenes. Show the script to the user and wait for approval before you render.
2. Animate each scene with Manim, or another code-driven animation tool that is installed.
3. Generate the narration audio. Use ElevenLabs when `ELEVENLABS_API_KEY` is set in the environment, and read the key only from that variable. Otherwise, use a local text-to-speech tool such as Kokoro, Piper, or macOS `say`.
4. Match each scene's length to its audio, then join video and audio with `ffmpeg`.

Done when the final video file plays, the narration matches the visuals, and you give the user its path.
