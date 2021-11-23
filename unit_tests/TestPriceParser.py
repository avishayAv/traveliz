import os
import unittest
from pathlib import Path

from TestsDB import Tests
from ParsingFunctions import parse_price


class TestPriceParser(unittest.TestCase):
    def test_parse_price(self):
        os.chdir(Path(os.getcwd()).parent)
        for test in Tests().tests:
            prices = parse_price(test.text, '', listing_price=None)
            prices = [x[0] for x in prices.values()]
            self.assertEqual(prices, test.price)


if __name__ == '__main__':
    unittest.main()
