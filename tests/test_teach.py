"""Unit tests for Digi Shell teach module."""

import tempfile
import unittest
from pathlib import Path
from digishell.teach import TeachManager


class TestTeachManager(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.teach = TeachManager(config_dir=self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_add_alias_rule(self):
        msg = self.teach.add_rule("sysinfo = uname -a")
        self.assertIn("sysinfo", msg)
        self.assertEqual(self.teach.match_rule("sysinfo"), "uname -a")

    def test_add_workflow_rule(self):
        msg = self.teach.add_rule("clean tmp -> rm -rf /tmp/*.log")
        self.assertIn("clean tmp", msg)
        self.assertEqual(self.teach.match_rule("clean tmp"), "rm -rf /tmp/*.log")


if __name__ == "__main__":
    unittest.main()
