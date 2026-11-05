# Testing a workflow and testing an agent

## Workflow

A workflow is deterministic, so test it like code.

- **Fixed cases:** the same input must give the same output. Keep a small set of inputs and expected results.
- **Failure paths:** force each step to fail and check the retry, the alert and the replay.
- **Idempotency:** run the same event twice. Nothing should be written twice.
- **Schema change:** rename a field in a test copy and see what breaks.

## Agent

An agent is not deterministic, so test the **behavior and the guardrails**, not exact text.

- **Golden cases:** a set of realistic tasks with a known right answer. Score the answer, the source it cited and the tools it used.
- **Refusal cases:** tasks it must not do (guess an order, edit a posted bill). It should stop and ask.
- **Guardrail tests:** a write with approval rejected must not run; an unknown tool must be blocked; a loop must stop at the step limit. See [`test_patterns.py`](../code/patterns/test_patterns.py).
- **Run it many times** on the same task. Look at the spread, not one good run.
- **Sandbox first**, then read-only on production, then writes with approval.

## Decide with data

Log what the agent did and where a person overrode it. When overrides stop, consider turning that decision into a workflow.
