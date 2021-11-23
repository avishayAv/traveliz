import unittest
from TestsDB import Tests
from ParsingFunctions import extract_dates_from_text

class TestDateParser(unittest.TestCase):
    def test_extract_dates_from_text(self):
        for test in Tests().tests:
            start_date, end_date = extract_dates_from_text(test.text)
            self.assertEqual(start_date, test.start_date)
            self.assertEqual(end_date, test.end_date)

if __name__ == '__main__':
    unittest.main()