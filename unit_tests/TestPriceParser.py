import unittest

from parameterized import parameterized

from ParsingFunctions import parse_price, parse_phone_number, extract_dates_from_text, extract_rooms_from_text
from TestsDB import Tests


class TestPriceParser(unittest.TestCase):
    @parameterized.expand(Tests().dump_prices_to_test())
    def test_parse_price(self, text, title, raw_price, gt_price, raw_location, group_id, parse_location, post_time):
        location = parse_location(title, text, listing_location=raw_location, group_id=group_id)
        rooms, masked_text = extract_rooms_from_text(text)
        start_date, end_date = extract_dates_from_text(masked_text, post_time)
        period = None if start_date is None or end_date is None else end_date - start_date

        price = parse_price(parse_phone_number(title, text)[1], listing_price=raw_price, city=location.city,
                            shared_apt=rooms.shared, period=period)
        # TODO [AA] : check how to assert a class using __eq__
        self.assertEqual(price.price_per_night, gt_price.price_per_night, msg=text)
        self.assertEqual(price.discounted_price_per_night, gt_price.discounted_price_per_night, msg=text)
        self.assertEqual(price.discounted_period, gt_price.discounted_period, msg=text)
        self.assertEqual(price.minimum_period, gt_price.minimum_period, msg=text)
        self.assertEqual(price.price_per_month, gt_price.price_per_month, msg=text)
        self.assertEqual(price.price_per_weekend, gt_price.price_per_weekend, msg=text)


if __name__ == '__main__':
    unittest.main()
