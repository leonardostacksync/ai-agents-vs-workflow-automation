"""Pattern 2: an agent loop with guardrails.

The model chooses the next step. The code around it decides what the model is
allowed to do. Swap `ScriptedModel` for a real model call; keep everything else.

Guardrails shown here:
  - an allow-list of tools, split into read tools and write tools
  - a step limit, so it cannot loop forever
  - an approval callback that must say yes before any write tool runs
  - an audit log of every decision
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Protocol


class Model(Protocol):
    def next(self, history: list[dict]) -> dict:
        """Return {"tool": name, "args": {...}} or {"final": text}."""


@dataclass
class ScriptedModel:
    """Stands in for a real model so the example runs offline and in tests."""

    script: list[dict]
    _i: int = 0

    def next(self, history: list[dict]) -> dict:
        out = self.script[min(self._i, len(self.script) - 1)]
        self._i += 1
        return out


@dataclass
class AgentResult:
    final: str | None
    steps: int
    log: list[str] = field(default_factory=list)
    stopped_because: str = "finished"


def run_agent(
    model: Model,
    read_tools: dict[str, Callable[..., object]],
    write_tools: dict[str, Callable[..., object]],
    approve: Callable[[str, dict], bool],
    max_steps: int = 8,
) -> AgentResult:
    history: list[dict] = []
    result = AgentResult(final=None, steps=0)

    for _ in range(max_steps):
        move = model.next(history)
        result.steps += 1

        if "final" in move:
            result.final = move["final"]
            result.log.append("final answer")
            return result

        name, args = move["tool"], move.get("args", {})

        if name in read_tools:
            out = read_tools[name](**args)
            result.log.append(f"read {name}({args})")
        elif name in write_tools:
            if not approve(name, args):
                result.log.append(f"write {name} REJECTED by reviewer")
                history.append({"tool": name, "error": "rejected"})
                continue
            out = write_tools[name](**args)
            result.log.append(f"write {name}({args}) approved")
        else:
            result.log.append(f"blocked unknown tool {name}")
            history.append({"tool": name, "error": "not allowed"})
            continue

        history.append({"tool": name, "args": args, "result": out})

    result.stopped_because = "step limit"
    result.log.append("stopped: step limit reached")
    return result
