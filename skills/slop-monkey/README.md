# Slop Monkey

A skill for turning formulaic agent output into direct, readable prose with a specific human voice.

This is a modified adaptation of [Stop Slop](https://github.com/hardikpandya/stop-slop) by [Hardik Pandya](https://hvpandya.com), not the original skill. It has a different name so users can distinguish this version from upstream.

## Contents

```text
slop-monkey/
├── SKILL.md
└── references/
    ├── examples.md
    ├── phrases.md
    └── structures.md
```

`SKILL.md` contains the editing workflow and completion checks. The reference files provide diagnostic catalogs and before-and-after examples; the skill loads them only when the draft needs that branch.

## Install

Install this repository's skills with:

```bash
npx skills add scottwater/skills
```

## Scope

The skill removes filler, canned rhetorical structures, vague emphasis, hidden agency, mechanical rhythm, and generic chatbot polish. It then strengthens audience awareness, concrete judgment, and the writer's existing cadence. Patterns remain diagnostic signals rather than universal bans, and every edit must preserve facts, confidence, intent, genre, and voice.

## Credits

The original **Stop Slop** skill was created by [Hardik Pandya](https://hvpandya.com). [Stop Slop's repository](https://github.com/hardikpandya/stop-slop) contains the upstream version.

This adaptation is maintained in `scottwater/skills`. Changes include a voice-contract editing workflow, explicit completion checks, and diagnostic references loaded as needed. It treats writing patterns as signals to inspect rather than universal bans, with an emphasis on preserving facts, confidence, genre, and the writer's voice.

The human-voice direction also draws from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [Lauren “poteto” Tan](https://x.com/poteto).

## License

[MIT](../../LICENSE)
