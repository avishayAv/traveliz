import unittest
import sys
sys.path.append('../')

from parameterized import parameterized

from ParsingFunctions import parse_phone_number
from TestsDB import Tests


class TestPhoneParser(unittest.TestCase):
    @parameterized.expand(Tests().dump_phones_to_test())
    def test_parse_phone(self, text, title, phone_number, source):
        if source == 'facebook':
            numbers = parse_phone_number(title, text)[0]
            if not phone_number:
                phone_number = set()
            self.assertSetEqual(numbers, phone_number)


if __name__ == '__main__':
    unittest.main()
