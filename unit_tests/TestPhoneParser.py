import os
import unittest
from pathlib import Path

from tqdm import tqdm

from TestsDB import Tests
from ParsingFunctions import ParseLocation, parse_phone_number


class TestLocationParser(unittest.TestCase):
    def test_parse_location(self):
        os.chdir(Path(os.getcwd()).parent)
        parse_location = ParseLocation()
        for i, test in tqdm(enumerate(Tests().tests)):
            numbers = parse_phone_number(test.raw_input.title, test.raw_input.text)[0]
            if not numbers:
                numbers = None

            self.assertEqual(numbers, test.gt.phone_number)



if __name__ == '__main__':
    unittest.main()
