import os
import unittest
from pathlib import Path

from TestsDB import Tests
from ParsingFunctions import parse_price, parse_phone_number

class TestPriceParser(unittest.TestCase):
    def test_parse_price(self):
        os.chdir(Path(os.getcwd()).parent)
        for test in Tests().tests:
            prices = parse_price(parse_phone_number(test.raw_input.title, test.raw_input.text)[1], listing_price=test.raw_input.price)
            prices = [x[0] for x in prices.values()]
            if test.gt.price is None:
                test.gt.price = []
            self.assertEqual(prices, test.gt.price)


if __name__ == '__main__':
    unittest.main()
