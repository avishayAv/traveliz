import datetime
import os
import pickle
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

from ParsingFunctions import ParseLocation
from Sublet import Rooms


@dataclass
class TestGroundTruth:
    start_date: datetime.date = None
    end_date: datetime.date = None
    price: {str: int} = None
    phone_number: set = None
    location: str = None
    rooms: Rooms = None


@dataclass
class TestRawInput:
    post_id: str = None
    title: str = None
    text: str = None
    post_time: datetime = None
    group_id: str = None
    location: str = None
    price: str = None
    phone_number: [str] = None


class Test:
    gt: TestGroundTruth
    raw_input: TestRawInput
    source: str

    def __init__(self, gt, raw_input, source):
        self.gt = gt
        self.raw_input = raw_input
        self.source = source

    def is_test_tagged(self):
        for field in self.gt.__dataclass_fields__:
            value = getattr(self.gt, field)
            if field != 'rooms' and field != 'price' and value is not None:
                return True
            if field == 'price':
                for price_field in value.__dataclass_fields__:
                    if price_field is not None:
                        return True
        return False


class Tests:
    def __init__(self, tests=None):
        if tests is None:
            tests = pickle.load(open('test_db.p', 'rb'))
        self.tests = tests

    def dump_dates_to_test(self):
        dates_tests = deepcopy(self.tests)
        dates_tests = [test for test in dates_tests if
                       "2/3/4 חדרים" not in test.raw_input.text and
                       "דירות 3 חדרים, 2 חדרים וסטודיו" not in test.raw_input.text and
                       "פיצוצייה 24/7" not in test.raw_input.text]
        # 2/3/4 - filter out generic posts for multiple sublet options
        # דירות 3 חדרים, 2 חדרים וסטודיו - filter out generic posts for multiple sublet options
        # 24/7 is being figures as a date
        return [(test.raw_input.text, test.gt.start_date, test.gt.end_date, test.raw_input.post_time, test.source)
                for test in dates_tests]

    def dump_rooms_to_test(self):
        rooms_tests = deepcopy(self.tests)
        rooms_tests = [test for test in rooms_tests if
                       "2/3/4 חדרים" not in test.raw_input.text and
                       "אננדה" not in test.raw_input.text]
        # 2/3/4 - filter out generic posts for multiple sublet options
        # ananda - מסבלט את חדרי הקסום בדירה מהממת ביפו. 200 מ' מהים. עם שותפות חמודות וגוד וייבז

        return [(test.raw_input.text, test.gt.rooms) for test in rooms_tests]

    def dump_phones_to_test(self):
        return [(test.raw_input.text, test.raw_input.title, test.gt.phone_number, test.source) for test in
                self.tests]

    def dump_prices_to_test(self):
        os.chdir(Path(os.getcwd()).parent)
        parse_location = ParseLocation()
        os.chdir(os.path.join(os.getcwd(), 'unit_tests'))
        return [(test.raw_input.text, test.raw_input.title, test.raw_input.price, test.gt.price,
                 test.raw_input.location, test.raw_input.group_id, parse_location, test.raw_input.post_time) for test in
                self.tests]

    def dump_locations_to_test(self):
        # TODO [YG] : remove all os.chdir from the code
        os.chdir(Path(os.getcwd()).parent)
        parse_location = ParseLocation()
        os.chdir(os.path.join(os.getcwd(), 'unit_tests'))
        return [(parse_location, test.raw_input.title, test.raw_input.text, test.raw_input.location,
                 test.raw_input.group_id, test.gt.location) for test in
                self.tests]
