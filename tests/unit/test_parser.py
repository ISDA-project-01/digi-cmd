"""
Unit tests for CommandParser
"""

import unittest
from digishell.core.parser import CommandParser

class TestCommandParser(unittest.TestCase):
    def test_parse_simple_command(self):
        parsed = CommandParser.parse("list all files")
        self.assertEqual(parsed.clean_text, "list all files")
        self.assertEqual(parsed.instructors, [])

    def test_cli_flags_preserved(self):
        parsed = CommandParser.parse("ls -la")
        self.assertEqual(parsed.clean_text, "ls -la")
        self.assertEqual(parsed.instructors, [])

        parsed_git = CommandParser.parse("git commit -m \"fix issue\"")
        self.assertEqual(parsed_git.clean_text, "git commit -m \"fix issue\"")

    def test_non_ai_prefix(self):
        parsed = CommandParser.parse("$dir")
        self.assertEqual(parsed.clean_text, "dir")
        self.assertTrue(parsed.has_instructor("$"))

    def test_instructors_extraction(self):
        parsed = CommandParser.parse("open app.py @disk D file app.py # ?")
        self.assertEqual(parsed.clean_text, "open app.py")
        self.assertTrue(parsed.has_instructor("@"))
        self.assertTrue(parsed.has_instructor("#"))
        self.assertTrue(parsed.has_instructor("?"))

if __name__ == "__main__":
    unittest.main()
