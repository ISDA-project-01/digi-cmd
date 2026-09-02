"""Unit tests for Digi Shell reinforcement and location resolution module."""

import unittest
from digishell.reinforcement import ReinforcementManager


class TestReinforcement(unittest.TestCase):

    def setUp(self):
        self.reinforcement = ReinforcementManager()

    def test_location_resolution(self):
        res = self.reinforcement.resolve_location("file LICENSE")
        self.assertIsNotNone(res)
        self.assertIn("LICENSE", res)

    def test_auto_fix_heuristic(self):
        fixed_cmd, reasoning = self.reinforcement.reinforce_and_fix(
            failed_cmd="python nonexistent.py",
            stdout="",
            stderr="python: command not found"
        )
        self.assertEqual(fixed_cmd, "python3 nonexistent.py")
        self.assertIn("python3", reasoning)


if __name__ == "__main__":
    unittest.main()
