import unittest
import sys
sys.path.append('../')

from parameterized import parameterized
from ParsingFunctions import extract_dates_from_text, extract_rooms_from_text
from TestsDB import Tests


class TestDateParser(unittest.TestCase):
    @parameterized.expand(Tests().dump_dates_to_test())
    def test_extract_dates_from_text(self, text, start_date, end_date, post_time, source):
        _, masked_text = extract_rooms_from_text(text)
        actual_start_date, actual_end_date = extract_dates_from_text(masked_text, post_time)
        if actual_start_date != start_date or actual_end_date != end_date:
            print (text)
        self.assertEqual(actual_start_date, start_date)
        if source != 'whatsapp':    # TODO [AA] : reconsider once NLP is done
            self.assertEqual(actual_end_date, end_date)


class TestRoomsParser(unittest.TestCase):
    @parameterized.expand(Tests().dump_rooms_to_test())
    def test_extract_rooms_from_text(self, text, rooms):
        actual_rooms, masked_text = extract_rooms_from_text(text)
        if actual_rooms.number != rooms.number or actual_rooms.shared != rooms.shared:
            print (text)
        self.assertEqual(actual_rooms.number, rooms.number)
        self.assertEqual(actual_rooms.shared, rooms.shared)



if __name__ == '__main__':
    unittest.main()
