"""Pattern 3: hybrid. A workflow for the known cases, an agent step for exceptions.

Invoices are matched by rule. Only the ones that do not match go to the agent,
and the agent can only *propose*. A person approves before anything is written.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Proposal:
    invoice_no: str
    action: str
    evidence: str


def exact_match(invoice: dict, purchase_orders: list[dict]) -> bool:
    return any(
        po["vendor"] == invoice["vendor"]
        and po["invoice_no"] == invoice["invoice_no"]
        and abs(po["amount"] - invoice["amount"]) < 0.01
        for po in purchase_orders
    )


def reconcile(
    invoices: list[dict],
    purchase_orders: list[dict],
    already_posted: set[str],
    propose: Callable[[dict], Proposal],
) -> dict:
    """Return what the workflow did and what is waiting for a person."""
    auto, queue, skipped = [], [], []

    for inv in invoices:
        key = f"{inv['vendor']}|{inv['invoice_no']}"
        if key in already_posted:              # duplicate check before any write
            skipped.append(inv["invoice_no"])
        elif exact_match(inv, purchase_orders):  # deterministic path
            auto.append(inv["invoice_no"])
        else:                                    # exception path: agent proposes
            queue.append(propose(inv))

    return {"auto_matched": auto, "needs_approval": queue, "skipped_duplicates": skipped}
