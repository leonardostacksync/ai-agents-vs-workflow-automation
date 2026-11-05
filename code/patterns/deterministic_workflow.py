"""Pattern 1: a deterministic workflow.

Fixed steps, retries, an idempotency key so a replay never double-writes, and a
log of every step. No model involved. Same input, same output.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable

Step = Callable[[dict], dict]


@dataclass
class Run:
    id: str
    status: str = "pending"
    log: list[str] = field(default_factory=list)
    failed_step: str | None = None


class Workflow:
    def __init__(self, steps: list[tuple[str, Step]], retries: int = 2, backoff: float = 0.0):
        self.steps = steps
        self.retries = retries
        self.backoff = backoff
        self._done: set[str] = set()  # idempotency keys already processed

    def run(self, run_id: str, payload: dict, idempotency_key: str | None = None) -> Run:
        run = Run(run_id)
        key = idempotency_key or run_id
        if key in self._done:
            run.status = "skipped"
            run.log.append(f"skipped: {key} already processed")
            return run

        data = dict(payload)
        for name, step in self.steps:
            for attempt in range(self.retries + 1):
                try:
                    data = step(data)
                    run.log.append(f"ok: {name}")
                    break
                except Exception as exc:  # noqa: BLE001 - a workflow records any failure
                    run.log.append(f"error: {name} attempt {attempt + 1}: {exc}")
                    if attempt == self.retries:
                        run.status = "failed"
                        run.failed_step = name
                        return run
                    time.sleep(self.backoff)

        self._done.add(key)
        run.status = "succeeded"
        return run

    def replay_from(self, failed_run: Run, payload: dict) -> Run:
        """Re-run only the steps from the failed one onward."""
        names = [n for n, _ in self.steps]
        start = names.index(failed_run.failed_step)
        tail = Workflow(self.steps[start:], self.retries, self.backoff)
        tail._done = self._done
        return tail.run(failed_run.id + "-replay", payload)


def match_invoice(data: dict) -> dict:
    """Rule: same vendor and invoice number, and amounts within a cent."""
    for po in data["purchase_orders"]:
        if po["vendor"] == data["vendor"] and po["invoice_no"] == data["invoice_no"]:
            data["matched"] = abs(po["amount"] - data["amount"]) < 0.01
            return data
    data["matched"] = False
    return data
