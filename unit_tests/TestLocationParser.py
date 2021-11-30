import os
import unittest
from pathlib import Path

from tqdm import tqdm

from TestsDB import Tests
from ParsingFunctions import ParseLocation


class TestLocationParser(unittest.TestCase):
    def test_parse_location(self):
        os.chdir(Path(os.getcwd()).parent)
        parse_location = ParseLocation()
        for i, test in tqdm(enumerate(Tests().tests)):
            location = parse_location(test.text, '', listing_location=None, group_id=None)
            self.assertEqual(location, test.location)


if __name__ == '__main__':
    unittest.main()
