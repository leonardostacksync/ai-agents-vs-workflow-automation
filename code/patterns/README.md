# The three patterns, in runnable code

Standard library only. Python 3.9 or newer. Run the tests:

```bash
python -m unittest -v
```

| File | Pattern | What it shows |
|---|---|---|
| [`deterministic_workflow.py`](deterministic_workflow.py) | Workflow | Fixed steps, retries, an idempotency key so a replay never writes twice, replay from the failed step |
| [`agent_loop.py`](agent_loop.py) | Agent | A model chooses the next step, the code limits it: tool allow-list, step limit, approval before any write, audit log |
| [`hybrid_pipeline.py`](hybrid_pipeline.py) | Hybrid | Rules handle the known cases, an agent only proposes for exceptions, duplicates are checked first |

`agent_loop.py` uses a `ScriptedModel` so it runs offline. To use a real model, write a class with a `next(history)` method that calls your model and returns either `{"tool": ..., "args": ...}` or `{"final": ...}`. Keep the guardrails exactly as they are.

These are teaching sketches, not a framework. They show where the control lives: in the code around the model.
