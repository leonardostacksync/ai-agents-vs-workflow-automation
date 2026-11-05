# Cost, speed and reliability

No numbers here on purpose. They depend on your volume, your model and your systems. Measure them in a pilot.

| | Workflow | Agent |
|---|---|---|
| Cost per run | Low and predictable | Higher, varies with the model and the number of steps |
| Speed | Fast | Slower, because each step may call a model |
| Same result each time | Yes | No |
| Handles unexpected input | Poorly | Better |
| Audit trail | Steps in a log | Steps in a log plus the reasoning evidence you require |
| Build effort | You write the rule | You write the job description and the guardrails |
| Maintenance | Update rules when systems change | Watch behavior, update instructions |

## How to think about cost

- Put volume in the workflow. A rule that runs thousands of times should not pay for a model every time.
- Use the agent where a person would otherwise spend minutes.
- Cap the agent: a step limit, a scope and a budget alert.
- Count the cost of a mistake too, not only the cost of a run. It is the reason for approval steps.

## How to think about reliability

Workflows are reliable when the rule is right. Agents are reliable when the task is narrow, the tools are limited, the evidence is cited and a person checks the risky writes.
