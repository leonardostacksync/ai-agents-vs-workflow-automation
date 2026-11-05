# Decision scorecard

`decide.py` turns seven yes/no questions into one of five answers: **workflow**, **workflow-first**, **hybrid**, **agent-first** or **agent**. It also flags when an approval step is needed.

```bash
python decide.py
python decide.py --json '{"rules_known": true, "input_structured": true, "must_be_repeatable": true, "steps_fixed": true, "needs_judgment": false, "tool_choice_varies": false, "high_volume": true, "writes_hard_to_undo": false}'
python -m unittest -v
```

The score is deliberately simple and visible. It is a prompt for a conversation, not an oracle. `cases.json` holds ten worked tasks with expected answers, so you can change the weights and see what moves. `decision-tree.mmd` is the same logic as a [Mermaid](https://mermaid.js.org) diagram.

Standard library only. Python 3.9 or newer.
