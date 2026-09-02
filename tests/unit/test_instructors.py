"""
Unit tests for Instructors
"""

import unittest
from digishell.core.context import ShellContext
from digishell.ai.client import AICommandEngine
from digishell.instructors.dispatcher import InstructorDispatcher

class TestInstructors(unittest.TestCase):
    def setUp(self):
        self.context = ShellContext()
        self.engine = AICommandEngine()
        self.dispatcher = InstructorDispatcher(self.context, self.engine)

    def test_teach_instructor(self):
        res = self.dispatcher.process_instructors([("!", "cls=clear")], "cls")
        self.assertIn("clear", self.context.learned_commands.get("cls", ""))

    def test_explain_instructor(self):
        res = self.dispatcher.process_instructors([("?", "")], "dir")
        self.assertEqual(len(res), 1)

if __name__ == "__main__":
    unittest.main()
