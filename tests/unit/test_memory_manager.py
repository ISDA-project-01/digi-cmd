"""
Unit tests for Memory Manager
"""

import unittest
from digishell.system.memory_manager import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def test_stats(self):
        stats = MemoryManager.get_memory_stats()
        self.assertIn("available_mb", stats)
        self.assertIn("mode", stats)

if __name__ == "__main__":
    unittest.main()
