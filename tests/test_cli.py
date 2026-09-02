"""Unit tests for Digi Shell CLI module."""

import unittest
from digishell.cli import DigiShellCLI


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.cli = DigiShellCLI()

    def test_cli_process_simple_command(self):
        # Should execute without throwing exception
        self.cli.process_command("echo Hello $")

    def test_cli_process_teach_command(self):
        self.cli.process_command("! hello_test = echo 'Hello World'")
        matched = self.cli.teach.match_rule("hello_test")
        self.assertEqual(matched, "echo 'Hello World'")


if __name__ == "__main__":
    unittest.main()
