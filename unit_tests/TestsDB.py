import datetime
import pickle
from copy import deepcopy
from dataclasses import dataclass

from Sublet import Rooms


@dataclass
class TestGroundTruth:
    start_date: datetime.date = None
    end_date: datetime.date = None
    price: {str: int} = None
    phone_number: [str] = None
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
            if field != 'rooms' and value is not None:
                return True
        return False


class Tests:
    def __init__(self, tests=None):
        if tests is None:
            tests = pickle.load(open('test_db.p', 'rb'))
        self.tests = tests

    def dump_dates_to_test(self):
        dates_tests = deepcopy(self.tests)
        return [(test.raw_input.text, test.gt.start_date, test.gt.end_date, test.raw_input.post_time.date()) for test in
                dates_tests]

    def dump_rooms_to_test(self):
        rooms_tests = deepcopy(self.tests)
        rooms_tests = [test for test in rooms_tests if "2/3/4 חדרים" not in test.raw_input.text]
        return [(test.raw_input.text, test.gt.rooms) for test in rooms_tests]
