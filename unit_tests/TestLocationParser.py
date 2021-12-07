import os
import unittest
from pathlib import Path

from tqdm import tqdm

from ParsingFunctions import ParseLocation
from TestsDB import Tests


class TestLocationParser(unittest.TestCase):
    def test_parse_location(self):
        tests = Tests().tests
        os.chdir(Path(os.getcwd()).parent)
        parse_location = ParseLocation()
        for i, test in tqdm(enumerate(tests)):
            location = parse_location(test.raw_input.title, test.raw_input.text,
                                      listing_location=test.raw_input.location, group_id=test.raw_input.group_id)
            self.assertEqual(location, test.gt.location)
        os.chdir(os.path.join(os.getcwd(), 'unit_tests'))


if __name__ == '__main__':
    unittest.main()
