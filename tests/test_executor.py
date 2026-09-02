"""Unit tests for Digi Shell command executor."""

import unittest
from digishell.executor import CommandExecutor


class TestExecutor(unittest.TestCase):

    def setUp(self):
        self.executor = CommandExecutor()

    def test_echo_command(self):
        res = self.executor.execute("echo 'DigiShell Test'")
        self.assertEqual(res.returncode, 0)
        self.assertIn("DigiShell Test", res.stdout)
        self.assertGreater(len(res.workflow_steps), 0)

    def test_cd_command(self):
        res = self.executor.execute("cd ..")
        self.assertEqual(res.returncode, 0)


if __name__ == "__main__":
    unittest.main()
