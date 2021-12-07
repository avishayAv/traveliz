import datetime
import pickle
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class TestGroundTruth:
    start_date: datetime = None
    end_date: datetime = None
    price: [int] = None
    phone_number: [str] = None
    location: str = None
    rooms: float = None


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

    def __init__(self, gt, raw_input):
        self.gt = gt
        self.raw_input = raw_input

    def is_test_tagged(self):
        for field in self.gt.__dataclass_fields__:
            value = getattr(self.gt, field)
            if value is not None:
                return True
        return False


class Tests:
    def __init__(self, tests=None):
        if tests is None:
            tests = pickle.load(open('test_db.p', 'rb'))
        self.tests = tests

    def dump_dates_to_test(self):
        dates_tests = deepcopy(self.tests)
        return [(test.raw_input.text, test.gt.start_date, test.gt.end_date, test.raw_input.post_time) for test in dates_tests]

