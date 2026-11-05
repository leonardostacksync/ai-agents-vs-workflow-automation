"""A small, explainable scorecard: workflow, AI agent, or both?

Answer seven yes/no questions about a task. The score is transparent on purpose,
so you can argue with it. Standard library only.

    python decide.py                 # interactive
    python decide.py --json '{"rules_known": true, ...}'
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass

# question key -> (prompt, (workflow points if yes, agent points if yes),
#                          (workflow points if no,  agent points if no))
QUESTIONS: dict[str, tuple[str, tuple[int, int], tuple[int, int]]] = {
    "rules_known": ("Can you write the full rule down in advance?", (2, 0), (0, 2)),
    "input_structured": ("Is the input structured fields, not free text or documents?", (1, 0), (0, 1)),
    "must_be_repeatable": ("Must the same input always give the same output?", (2, 0), (0, 0)),
    "steps_fixed": ("Is the sequence of steps the same every time?", (2, 0), (0, 2)),
    "needs_judgment": ("Does each case need interpretation or judgment?", (0, 2), (1, 0)),
    "tool_choice_varies": ("Does the right system or tool to use change per case?", (0, 2), (1, 0)),
    "high_volume": ("Is it high volume, where cost per run matters?", (1, 0), (0, 0)),
}

LABELS = {
    "workflow": "Use a workflow.",
    "workflow-first": "Use a workflow, and add an agent step only for the exceptions.",
    "hybrid": "Use both: a workflow for the fixed parts and an agent for the judgment.",
    "agent-first": "Use an agent, with a workflow around it for the fixed parts and the guardrails.",
    "agent": "Use an agent.",
}


@dataclass
class Result:
    label: str
    workflow_score: int
    agent_score: int
    approval_required: bool
    reasons: list[str]

    @property
    def advice(self) -> str:
        return LABELS[self.label]


def decide(answers: dict[str, bool], writes_hard_to_undo: bool = False) -> Result:
    missing = [k for k in QUESTIONS if k not in answers]
    if missing:
        raise ValueError(f"missing answers: {', '.join(missing)}")

    wf = ag = 0
    reasons: list[str] = []
    for key, (prompt, yes_pts, no_pts) in QUESTIONS.items():
        w, a = yes_pts if answers[key] else no_pts
        wf += w
        ag += a
        if w or a:
            side = "workflow" if w > a else "agent"
            reasons.append(f"{'Yes' if answers[key] else 'No'}: {prompt} (+{max(w, a)} {side})")

    if ag <= 1:
        label = "workflow"
    elif wf <= 1:
        label = "agent"
    elif wf - ag >= 3:
        label = "workflow-first"
    elif ag - wf >= 3:
        label = "agent-first"
    else:
        label = "hybrid"

    return Result(label, wf, ag, writes_hard_to_undo, reasons)


def _ask(prompt: str) -> bool:
    while True:
        raw = input(f"{prompt} [y/n] ").strip().lower()
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="answers as a JSON object")
    args = parser.parse_args()

    if args.json:
        data = json.loads(args.json)
        hard = bool(data.pop("writes_hard_to_undo", False))
        result = decide(data, hard)
    else:
        answers = {k: _ask(q[0]) for k, q in QUESTIONS.items()}
        result = decide(answers, _ask("Are the writes hard to undo?"))

    print(f"\n{result.advice}")
    print(f"workflow score {result.workflow_score}, agent score {result.agent_score}")
    for line in result.reasons:
        print(f"  - {line}")
    if result.approval_required:
        print("Add an approval step before any write that is hard to undo.")


if __name__ == "__main__":
    main()
