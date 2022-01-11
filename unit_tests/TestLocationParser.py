import unittest

from parameterized import parameterized

from TestsDB import Tests


class TestLocationParser(unittest.TestCase):
    @parameterized.expand(Tests().dump_locations_to_test())
    def test_parse_location(self, parse_location, title, text, raw_location, group_id, gt_location):
        location = parse_location(title, text,
                                  listing_location=raw_location, group_id=group_id)
        self.assertEqual(gt_location, location.city,
                         msg=f'title: {title} \n text: {text} \n raw_location: {raw_location} \n group_id: {group_id}')


if __name__ == '__main__':
    unittest.main()
