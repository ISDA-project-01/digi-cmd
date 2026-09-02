"""Unit tests for Digi Shell command parser."""

import unittest
from digishell.parser import parse_input


class TestParser(unittest.TestCase):

    def test_direct_execution_flag(self):
        res = parse_input("ls -la $")
        self.assertEqual(res.clean_prompt, "ls -la")
        self.assertTrue(res.direct_execution)
        self.assertIn('$', res.instructors)

    def test_location_instructor(self):
        res = parse_input("open app.py @ disk may be D and file app.py")
        self.assertEqual(res.clean_prompt, "open app.py")
        self.assertEqual(res.location, "disk may be D and file app.py")
        self.assertIn('@', res.instructors)

    def test_teach_instructor(self):
        res = parse_input("! sysinfo = uname -a")
        self.assertEqual(res.teach, "sysinfo = uname -a")
        self.assertIn('!', res.instructors)

    def test_multiple_flags(self):
        res = parse_input("scan local network ? ; * - # ^")
        self.assertEqual(res.clean_prompt, "scan local network")
        self.assertTrue(res.help)
        self.assertTrue(res.workflow)
        self.assertTrue(res.justify)
        self.assertTrue(res.explain)
        self.assertTrue(res.autofix)
        self.assertTrue(res.install)


if __name__ == "__main__":
    unittest.main()
