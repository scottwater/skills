# AI Lens

Prompt injection, tool abuse, tenant leakage, and unsafe model output in Rails AI features.

## Map

```bash
grep -rn "OpenAI\|Anthropic\|RubyLLM\|ruby_llm\|ruby-openai\|Langchain\|langchain\|chat\.completions\|messages\.create\|system_prompt\|prompt" app/ lib/ Gemfile.lock
grep -rn "embedding\|pgvector\|nearest_neighbors\|similarity\|retrieval\|chunk" app/ lib/ db/
grep -rn "tool_call\|function_call\|MCP\|ModelContext" app/ lib/
```

When nothing hits, return no findings and state the patterns checked.

For each integration, document: prompt construction, untrusted inputs (user text, records, uploads, ActionMailbox, RAG chunks, tool output), tools the model can call, the identity used for data access, tenant scoping at retrieval/generation/tool time, and output sinks.

## Search

- Untrusted content interpolated into prompts without delimiting; prompt wording treated as the security boundary instead of Rails-side permission checks.
- Retrieval and tools running above the requesting user: RAG queries without account or policy scoping; background jobs doing AI work as a global service account; a lower-privileged user's stored content consumed by an admin's assistant session.
- Tools: each tool allowlisted, arguments validated, guarded by the same authorization as the equivalent direct user action, human approval on destructive actions (email, charges, role changes, data export, code or SQL execution), iteration and rate budgets, audit logs of actor, tenant, tool, and result.
- Secrets or PII in prompts; prompt templates stored in user-editable records; full prompts and completions logged with credentials.
- Model output rendered through `raw`/`.html_safe`/ActionText/Markdown without an allowlist sanitizer; generated SQL, shell commands, or code executed; generated URLs used in `redirect_to` or links.
- Memory and embeddings scoped per user and tenant; authorization re-checked at retrieval time, not only at indexing; vectors deleted or reindexed when source permissions change.

## Evidence bar

Who can plant the input, which boundary it crosses — tenant, privilege, or output sink — and the code path, with `file:lines`.

## Exclude

Provider-side configuration, and prompt-quality advice with no security consequence.
