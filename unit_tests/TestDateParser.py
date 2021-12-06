import unittest

from parameterized import parameterized

from ParsingFunctions import extract_dates_from_text
from TestsDB import Tests


class TestDateParser(unittest.TestCase):
    @parameterized.expand(Tests().dump_dates_to_test())
    def test_extract_dates_from_text(self, text, start_date, end_date, post_time):
        actual_start_date, actual_end_date = extract_dates_from_text(text, post_time)
        self.assertEqual(actual_start_date, start_date)
        self.assertEqual(actual_end_date, end_date)


# patterns = DatePatterns().patterns
# range_to_dates_tests = [DateReg('31.12.21-31.03', patterns[3], DateSeperator.DOT),
#                         DateReg('31/12/21-31/03', patterns[3], DateSeperator.SLASH),
#                         DateReg('31\\12\\21-31\\03', patterns[3], DateSeperator.BACKSLASH),
#                         DateReg('1.12.21-31.12', patterns[3], DateSeperator.DOT),
#                         DateReg('1/12/21-31/12', patterns[3], DateSeperator.SLASH),
#                         DateReg('1\\12\\21-31\\12', patterns[3], DateSeperator.BACKSLASH)
#                         ]


if __name__ == '__main__':
    unittest.main()
