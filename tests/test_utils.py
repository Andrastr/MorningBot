"""
test module for testing utils module
"""
import unittest
from datetime import datetime
from dataclasses import dataclass
import utils

@dataclass
class User:
    """
    represents user that sent message
    """
    name: str
    mention: str
    bot: bool

@dataclass
class Message:
    """
    represents message that was sent
    """
    author: User
    content: str

class TestCalculateTimezone(unittest.TestCase):
    """
    Tests for calculate_timezone function
    """
    def test_datetime_after_morning(self):
        """
        Tests datetime after morning
        """
        now = datetime.now()
        now = now.replace(hour=15, minute=0, second=0, microsecond=0)
        morning = now.replace(hour=8)

        value = utils.calculate_timezone(now,morning)

        self.assertEqual(value, -7, "Should be -7")

    def test_datetime_before_morning(self):
        """
        Tests datetime before morning
        """
        now = datetime.now()
        now = now.replace(hour=7, minute=0, second=0, microsecond=0)
        morning = now.replace(hour=8)

        value = utils.calculate_timezone(now,morning)

        self.assertEqual(value, 1, "Should be 1")

    def test_datetime_equals_morning(self):
        """
        Tests datetime at start of morning
        """
        now = datetime.now()
        now = now.replace(hour=8, minute=0, second=0, microsecond=0)
        morning = now.replace(hour=8)

        value = utils.calculate_timezone(now,morning)

        self.assertEqual(value, 0, "Should be 0")

class TestGetLocation(unittest.TestCase):
    """
    Tests for get_location function
    """
    def test_get_location_00(self):
        """
        Test get_location with timezone 0 and random_number 0
        """
        timezone = 0
        random_number = 0

        location = utils.get_location(timezone,random_number)

        self.assertEqual(location, "Cockermouth", "Should be Cockermouth")

    def test_get_location_02(self):
        """
        Test get_location with timezone 0 and random_number 2
        """
        timezone = 0
        random_number = 2

        location = utils.get_location(timezone,random_number)

        self.assertEqual(location, "(تجكجة (Tidjikja)", "Should be (تجكجة (Tidjikja)")

class TestGetResponse(unittest.TestCase):
    """
    Tests for get_response function
    """
    def test_get_response_bore_jam(self):
        """
        Test get_response with trigger bore, and author jam
        """
        author = User("Jam", "@284848", False)
        message = Message(author, "bore da")
        trigger_values = utils.get_language_return_type(message)
        location = "Wales"

        response = utils.get_response(message, trigger_values, location)

        self.assertEqual(response, "@284848 Bore da o Wales")

    def test_get_response_morning_jam(self):
        """
        Test get_response with trigger morning, and author Jam
        """
        author = User("Jam", "@284848", False)
        message = Message(author, "good morning folks")
        trigger_values = utils.get_language_return_type(message)
        location = "Wales"

        response = utils.get_response(message, trigger_values, location)

        self.assertEqual(response, "@284848 Good morning from Wales")

    def test_get_response_gninrom_jam(self):
        """
        Test get_response with trigger gninrom, and author Jam
        """
        author = User("Jam", "@284848", False)
        message = Message(author, "gninrom doog")
        trigger_values = utils.get_language_return_type(message)
        location = "Wales"

        response = utils.get_response(message, trigger_values, location)

        self.assertEqual(response, "selaW morf gninrom dooG maJ@")

    def test_get_response_no_vals(self):
        """
        Test get_response with no values
        """
        author = User("", "", False)
        message = Message(author, "")
        trigger_values = utils.get_language_return_type(message)
        location = ""

        response = utils.get_response(message, trigger_values, location)

        self.assertEqual(response, None)

if __name__ == '__main__':
    unittest.main()
