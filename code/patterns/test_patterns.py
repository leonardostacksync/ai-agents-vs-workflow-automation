import unittest

from agent_loop import ScriptedModel, run_agent
from deterministic_workflow import Workflow, match_invoice
from hybrid_pipeline import Proposal, reconcile

POS = [{"vendor": "Acme", "invoice_no": "A-1", "amount": 100.0}]


class WorkflowTests(unittest.TestCase):
    def test_same_input_same_output(self):
        wf = Workflow([("match", match_invoice)])
        payload = {"vendor": "Acme", "invoice_no": "A-1", "amount": 100.0, "purchase_orders": POS}
        self.assertEqual(wf.run("r1", payload).status, "succeeded")

    def test_idempotency_key_prevents_a_second_write(self):
        calls = []
        wf = Workflow([("write", lambda d: calls.append(1) or d)])
        wf.run("r1", {}, idempotency_key="k")
        second = wf.run("r2", {}, idempotency_key="k")
        self.assertEqual(second.status, "skipped")
        self.assertEqual(len(calls), 1)

    def test_retries_then_fails_and_replays_only_the_failed_step(self):
        state = {"n": 0}

        def flaky(d):
            state["n"] += 1
            if state["n"] < 10:
                raise RuntimeError("api down")
            return d

        seen = []
        wf = Workflow([("first", lambda d: seen.append("first") or d), ("flaky", flaky)], retries=1)
        failed = wf.run("r1", {})
        self.assertEqual((failed.status, failed.failed_step), ("failed", "flaky"))
        state["n"] = 20  # the API is back
        replay = wf.replay_from(failed, {})
        self.assertEqual(replay.status, "succeeded")
        self.assertEqual(seen, ["first"])  # first step was not repeated


class AgentTests(unittest.TestCase):
    def test_write_needs_approval(self):
        writes = []
        model = ScriptedModel([{"tool": "credit", "args": {"amount": 5}}, {"final": "done"}])
        res = run_agent(model, {}, {"credit": lambda amount: writes.append(amount)}, lambda n, a: False)
        self.assertEqual(writes, [])
        self.assertIn("REJECTED", " ".join(res.log))

    def test_approved_write_runs(self):
        writes = []
        model = ScriptedModel([{"tool": "credit", "args": {"amount": 5}}, {"final": "done"}])
        run_agent(model, {}, {"credit": lambda amount: writes.append(amount)}, lambda n, a: True)
        self.assertEqual(writes, [5])

    def test_unknown_tool_is_blocked(self):
        model = ScriptedModel([{"tool": "drop_table"}, {"final": "x"}])
        res = run_agent(model, {}, {}, lambda n, a: True)
        self.assertIn("blocked unknown tool drop_table", res.log)

    def test_step_limit_stops_a_loop(self):
        model = ScriptedModel([{"tool": "look", "args": {}}])  # repeats forever
        res = run_agent(model, {"look": lambda: 1}, {}, lambda n, a: True, max_steps=3)
        self.assertEqual((res.steps, res.stopped_because), (3, "step limit"))


class HybridTests(unittest.TestCase):
    def test_known_cases_skip_the_agent(self):
        asked = []
        invoices = [
            {"vendor": "Acme", "invoice_no": "A-1", "amount": 100.0},   # exact match
            {"vendor": "Acme", "invoice_no": "A-2", "amount": 50.0},    # exception
            {"vendor": "Acme", "invoice_no": "A-0", "amount": 10.0},    # duplicate
        ]

        def propose(inv):
            asked.append(inv["invoice_no"])
            return Proposal(inv["invoice_no"], "review", "no purchase order found")

        out = reconcile(invoices, POS, {"Acme|A-0"}, propose)
        self.assertEqual(out["auto_matched"], ["A-1"])
        self.assertEqual(out["skipped_duplicates"], ["A-0"])
        self.assertEqual(asked, ["A-2"])
        self.assertEqual(len(out["needs_approval"]), 1)


if __name__ == "__main__":
    unittest.main()
