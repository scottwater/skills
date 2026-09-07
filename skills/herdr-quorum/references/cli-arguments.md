# CLI arguments

Translate `cli|model|reasoning` into native arguments after Herdr's `--` separator:

```sh
herdr agent start <unique-name> --kind <cli> --pane <pane-id> -- <native-arguments>
```

These mappings are the launch contract, implemented by the [launcher](../scripts/launch.py). Use them directly with fresh interactive conversations and each CLI's normal configuration, credentials, project instructions, and permissions. Launch once; preserve errors for maintenance rather than validating or repairing the environment during a run.

| CLI | Model argument | Reasoning argument |
| --- | --- | --- |
| `pi` | `--model '<provider/model>'` | `--thinking '<reasoning>'` |
| `codex` | `--model '<model>'` | `-c 'model_reasoning_effort="<reasoning>"'` |
| `claude` | `--model '<model-or-alias>'` | `--effort '<reasoning>'` |

For `default` reasoning, omit the reasoning argument. Preserve the full model field, including provider prefixes and slashes. Profiles must supply exact Pi identifiers rather than fuzzy patterns. Trust the requested identifier at launch; availability and authentication are established only by execution, not by these mappings. Report any observed model or reasoning mismatch as a worker failure.

Keep tuple fields as data: pass separate arguments, or shell-quote each value when constructing a command. The tuple's pipes are delimiters, never shell operators.

An unmapped CLI fails input validation before panes are created. Adding one is a separate maintenance task: establish its Herdr kind and interactive model/reasoning arguments from installed help or authoritative documentation, then update this contract, the launcher, and its tests together. Help calls, model listings, configuration searches, and compatibility repairs belong only to an explicitly requested diagnostic or maintenance task.
