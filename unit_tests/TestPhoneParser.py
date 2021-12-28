import unittest

from tqdm import tqdm

from ParsingFunctions import parse_phone_number
from TestsDB import Tests


class TestPhoneParser(unittest.TestCase):
    def test_parse_phone(self):
        for i, test in tqdm(enumerate(Tests().tests)):
            if test.source == 'facebook':
                numbers = parse_phone_number(test.raw_input.title, test.raw_input.text)[0]
                if not test.gt.phone_number:
                    test.gt.phone_number = set()
                self.assertSetEqual(set(numbers), set(test.gt.phone_number))


if __name__ == '__main__':
    unittest.main()
