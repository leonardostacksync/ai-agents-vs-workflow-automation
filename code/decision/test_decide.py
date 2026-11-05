import json
import pathlib
import unittest

from decide import QUESTIONS, decide

CASES = json.loads((pathlib.Path(__file__).parent / "cases.json").read_text())


class DecideTests(unittest.TestCase):
    def test_every_case_matches_its_expected_label(self):
        for case in CASES:
            with self.subTest(task=case["task"]):
                result = decide(case["answers"], case["writes_hard_to_undo"])
                self.assertEqual(result.label, case["expected"], result.reasons)

    def test_missing_answer_is_an_error(self):
        with self.assertRaises(ValueError):
            decide({"rules_known": True})

    def test_approval_flag_follows_irreversible_writes(self):
        answers = {k: True for k in QUESTIONS}
        self.assertTrue(decide(answers, True).approval_required)
        self.assertFalse(decide(answers, False).approval_required)


if __name__ == "__main__":
    unittest.main()
