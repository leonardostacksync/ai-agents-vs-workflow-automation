# How each one fails

## Workflows

| Failure | What it looks like | Mitigation |
|---|---|---|
| Brittle to change | A field is renamed and every run fails | Alert on failures, version the workflow, test against schema changes |
| Silent failure | It stops and nobody notices | Failure alerts and a log you read |
| Repeated side effects | A retry or replay writes twice | Idempotency keys, look up before writing |
| Wrong rule, applied perfectly | It is consistent and consistently wrong | Review the rule, sample outputs |
| Cannot handle the unexpected | Edge cases pile up in an exceptions table | Route exceptions to a person or an agent step |

## AI agents

| Failure | What it looks like | Mitigation |
|---|---|---|
| Made-up values | A field or record that does not exist | Require a cited source for every fact, check against the system |
| Wrong tool | It writes where it should have read | Tool allow-list, separate read and write tools |
| Loops | It repeats the same call | Step limit, stop on no progress |
| Over-reach | It does more than asked | Narrow job description, "never does" list |
| Duplicate writes | It creates a record that exists | Check for the record before every write |
| Hard to reproduce | Same input, different output | Log every step, keep evidence, test with fixed cases |

## Both

- **Unlogged runs.** If you cannot see what ran, you cannot trust it.
- **Writes with no approval** on a hard-to-undo action.
- **No sandbox test** before production data.

The pattern code in [`code/patterns`](../code/patterns/README.md) shows several of these mitigations.
