"""
Unit tests for Location Resolver
"""

import unittest
from digishell.reinforcement.location_resolver import LocationResolver

class TestLocationResolver(unittest.TestCase):
    def test_parse_drive_and_file(self):
        res = LocationResolver.resolve_location("disk may be D and file app.py")
        self.assertIsNotNone(res)

if __name__ == "__main__":
    unittest.main()
