"""
Unit tests for AI Command Engine
"""

import unittest
from digishell.ai.client import AICommandEngine

class TestAIEngine(unittest.TestCase):
    def test_offline_translation(self):
        engine = AICommandEngine()
        cmd_win = engine.translate_natural_language("list files", "windows")
        self.assertEqual(cmd_win, "dir")

        cmd_linux = engine.translate_natural_language("list files", "linux")
        self.assertEqual(cmd_linux, "ls -la")

if __name__ == "__main__":
    unittest.main()
