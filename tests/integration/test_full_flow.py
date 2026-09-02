"""
Integration test for full execution flow
"""

import unittest
from digishell.core.context import ShellContext
from digishell.core.parser import CommandParser
from digishell.executors.shell import CommandExecutor

class TestIntegration(unittest.TestCase):
    def test_end_to_end_parsed_exec(self):
        parsed = CommandParser.parse("$ echo Hello DigiShell")
        code, stdout, stderr = CommandExecutor.execute(parsed.clean_text)
        self.assertEqual(code, 0)
        self.assertIn("Hello DigiShell", stdout)

if __name__ == "__main__":
    unittest.main()
