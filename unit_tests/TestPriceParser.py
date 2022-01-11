import unittest

from parameterized import parameterized

from ParsingFunctions import parse_price, parse_phone_number
from TestsDB import Tests


class TestPriceParser(unittest.TestCase):
    @parameterized.expand(Tests().dump_prices_to_test())
    def test_parse_price(self, text, title, raw_price, gt_price):
        prices = parse_price(parse_phone_number(title, text)[1],
                             listing_price=raw_price)
        prices = [x[0] for x in prices.values()]
        if gt_price is None:
            gt_price = set()
        else:
            gt_price = set(gt_price.values())
        self.assertSetEqual(set(prices), gt_price, msg=text)


if __name__ == '__main__':
    unittest.main()
