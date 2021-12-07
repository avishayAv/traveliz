import unittest

from tqdm import tqdm

from ParsingFunctions import parse_phone_number
from TestsDB import Tests


class TestLocationParser(unittest.TestCase):
    def test_parse_location(self):
        for i, test in tqdm(enumerate(Tests().tests)):
            numbers = parse_phone_number(test.raw_input.title, test.raw_input.text)[0]
            if not numbers:
                numbers = None

            self.assertEqual(numbers, test.gt.phone_number)

if __name__ == '__main__':
    unittest.main()
