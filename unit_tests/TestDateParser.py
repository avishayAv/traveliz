import unittest

from parameterized import parameterized

from ParsingFunctions import extract_dates_from_text, extract_rooms_from_text
from TestsDB import Tests


class TestDateParser(unittest.TestCase):
    @parameterized.expand(Tests().dump_dates_to_test())
    def test_extract_dates_from_text(self, text, start_date, end_date, post_time):
        _, masked_text = extract_rooms_from_text(text)
        actual_start_date, actual_end_date = extract_dates_from_text(masked_text, post_time)
        self.assertEqual(actual_start_date, start_date)
        self.assertEqual(actual_end_date, end_date)


class TestRoomsParser(unittest.TestCase):
    @parameterized.expand(Tests().dump_rooms_to_test())
    def test_extract_rooms_from_text(self, text, rooms):
        actual_rooms, masked_text = extract_rooms_from_text(text)
        self.assertEqual(actual_rooms, rooms)


if __name__ == '__main__':
    unittest.main()
