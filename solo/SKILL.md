---
name: solo
description: Use when the user asks to use Solo (MCP) to spawn coding agents, manage scratchpads, todos, or timers, or to inspect Solo-managed processes.
---

# Solo

Solo is a desktop application for managing coding agents and project-scoped coordination state. It is reached only through its MCP server — there is no Solo CLI.

## Pi behavior

If running under Pi, detected by `PI_CODING_AGENT=true`, use the `pi-soloterm` extension tools for Solo MCP server features:

- `solo_status` — verify SoloTerm/MCP availability, identity, and feature support.
- `solo_task` — spawn Solo-managed coding agents/processes and send them prompts. For parallel work, use one call with `tasks: [...]`.
- `solo_scratchpad` — list, read, or write Solo scratchpads.
- `solo_todo` — manage Solo todos when available, with Pi session fallback.

Call `solo_status` first. If it reports ready, proceed with the relevant `solo_*` tool — these tools are full Solo MCP support under Pi; `pi-soloterm` is the bridge.

If a required `solo_*` tool is missing, tell the user to install/enable `pi-soloterm`. If `solo_status` reports Solo MCP unavailable, tell the user to run Solo and enable **Settings → MCP**.

## Non-Pi behavior

If not running under Pi, use the current harness's Solo MCP tools directly. If exact tool names are unclear, inspect the MCP tool catalog.

## Feature tools

Beyond core project/process management, Solo exposes optional feature tools — scratchpads, todos, timers, and key-value storage — gated by Solo settings. Scratchpads, todos, and timers usually inherit MCP server enablement; key-value tools may need to be enabled separately. Discover the exact tools from the MCP catalog.

## Spawned agents

When spawning a new agent, monitor it for questions and permission requests; approve only requests needed to complete the prompt you gave it.
