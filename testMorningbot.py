import unittest
from datetime import datetime, timedelta,date
import utils

class TestCalculateTimezone(unittest.TestCase):
    def test_datetime_after_morning(self):
        now = datetime.now()
        now = now.replace(hour=15, minute=0, second=0, microsecond=0)
        morning = now.replace(hour=8)

        value = utils.calculate_timezone(now,morning)

        self.assertEqual(value, -7, "Should be -7")
    
    def test_datetime_before_morning(self):
        now = datetime.now()
        now = now.replace(hour=7, minute=0, second=0, microsecond=0)
        morning = now.replace(hour=8)

        value = utils.calculate_timezone(now,morning)

        self.assertEqual(value, 1, "Should be 1")

    def test_datetime_equals_morning(self):
        now = datetime.now()
        now = now.replace(hour=8, minute=0, second=0, microsecond=0)
        morning = now.replace(hour=8)

        value = utils.calculate_timezone(now,morning)

        self.assertEqual(value, 0, "Should be 0")
    
class TestGetLocation(unittest.TestCase):
    def test_get_location_00(self):
        timezone = 0
        random_number = 0

        location = utils.get_location(timezone,random_number)

        self.assertEqual(location, "Cockermouth", "Should be Cockermouth")

    def test_get_location_02(self):
        timezone = 0
        random_number = 2

        location = utils.get_location(timezone,random_number)

        self.assertEqual(location, "(تجكجة (Tidjikja)", "Should be (تجكجة (Tidjikja)")

if __name__ == '__main__':
    unittest.main()