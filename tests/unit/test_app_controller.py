"""
Unit test for app_controller
"""

import unittest
import sys
from unittest.mock import patch
from digishell.agentic.app_controller import AppController

class TestAppController(unittest.TestCase):
    @patch("subprocess.Popen")
    def test_open_app(self, mock_popen):
        msg = AppController.open_application("echo_test")
        self.assertIn("echo_test", msg)

if __name__ == "__main__":
    unittest.main()
