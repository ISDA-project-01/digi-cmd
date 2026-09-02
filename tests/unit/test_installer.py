"""
Unit test for installer
"""

import unittest
from digishell.executors.installer import AutoInstaller

class TestAutoInstaller(unittest.TestCase):
    def test_empty_target(self):
        res = AutoInstaller.install_or_update("")
        self.assertEqual(res, "No package specified for installation.")

if __name__ == "__main__":
    unittest.main()
