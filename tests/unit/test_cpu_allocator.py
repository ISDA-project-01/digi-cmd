"""
Unit test for cpu_allocator
"""

import unittest
from digishell.system.cpu_allocator import CpuOptimizer

class TestCpuOptimizer(unittest.TestCase):
    def test_priority(self):
        msg = CpuOptimizer.optimize_process_priority()
        self.assertIsNotNone(msg)

if __name__ == "__main__":
    unittest.main()
