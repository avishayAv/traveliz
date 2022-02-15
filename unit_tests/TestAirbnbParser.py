import unittest
import sys
sys.path.append('../')

from parameterized import parameterized
from AirbnbUtils import AirbnbParser
from datetime import datetime
import pickle

class airbnb_data_for_test():
    def __init__(self):
        self.ids_for_calander_test = ['2901581', '51096878', '51455920']
        self.month = datetime.now().month
        self.year = datetime.now().year

    def id_month_year(self):
        return [[id, str(self.month), str(self.year)] for id in self.ids_for_calander_test]


class TestAirbnbParser(unittest.TestCase):
    @parameterized.expand(airbnb_data_for_test().id_month_year())
    def test_airbnb_get_calendar(self, id, month, year):
        calendar = AirbnbParser.get_calendar_of_airbnb_listing_id(id, month=month, year=year)
        self.assertNotEqual(calendar, []), f"calander shouldn't be empty"


    @parameterized.expand([[x] for x in pickle.load(open("../test_airbnb_db.p", "rb"))])
    def test_airbnb_parser(self,listing):
        self.assertNotEqual(listing, None), f"listing shouldn't be None"
        self.assertNotEqual(listing.location, "")
        assert "airbnb" in listing.post_url


if __name__ == '__main__':
    unittest.main()