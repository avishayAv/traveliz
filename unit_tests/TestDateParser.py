import unittest
from TestsDB import Tests
from ParsingFunctions import extract_dates_from_text
from parameterized import parameterized

class TestDateParser(unittest.TestCase):
    @parameterized.expand(Tests().dump_dates_to_test())

    def test_extract_dates_from_text(self, text, start_date, end_date):
        actual_start_date, actual_end_date = extract_dates_from_text(text)
        self.assertEqual(actual_start_date, start_date)
        self.assertEqual(actual_end_date, end_date)

if __name__ == '__main__':
    unittest.main()