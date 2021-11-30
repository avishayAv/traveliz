import datetime
from enum import Enum

import dateutil
import dateutil.parser as dparser


# Hebrew -> hex unicode
def get_hex_unicode(reg_str):
    uni_str = ''
    for letter in reg_str:
        uni_str += r'\u0'
        uni_str += f'{hex(ord(letter)).split("x")[1]}'
    return uni_str


# TODO [AA] : support whitespaces in all tests patterns
class DatePatterns:
    def __init__(self):
        self.patterns = [
            DatePattern("combined_full_start_end_pattern1", "\d+[-]\d+[/.]\d+[/.]\d+", True, True),  # DD-DD/MM/YY
            DatePattern("combined_full_start_end_pattern2",
                        "\d+\s*[\\\\/.]\s*\d+\s*[\\\\/.]\s*\d+\s*[-]\s*\d+\s*[\\\\/.]\s*\d+\s*[\\\\/.]\s*\d+", True,
                        True),
            # DD/MM/YY-DD/MM/YY
            DatePattern("combined_full_start_end_pattern3", "\d+[/.]\d+[-]\d+[/.]\d+[/.]\d+", True, True),
            # DD/MM-DD/MM/YY
            DatePattern("combined_full_start_end_pattern4", "\d+[/.]\d+[/.]\d+[-]\d+[/.]\d+", True, True),
            # DD/MM/YY-DD/MM
            DatePattern("combined_full_start_end_pattern5", "\d+[/.]\d+[-]\d+[/.]\d+", False, True),  # DD/MM-DD/MM
            DatePattern("combined_part_start_end_pattern2", "\d+[-]\d+[/.]\d+", False, True),  # D-D/M
            DatePattern("full_date_pattern", "\d+[/.]\d+[/.]\d+", True, False),
            # D/M/YY, D/M/YYYY, DD/M/YY, DD/M/YYYY, D/MM/YY, D/MM/YYYY, DD/MM/YY, DD/MM/YYYY
            DatePattern("part_date_pattern", "\d+[/.]\d+", False, False),  # D/M, DD/M, D/MM, DD/MM
            DatePattern("part_date_half_hebrew_pattern",
                        ("(\d+\s+" + DatePatterns.get_relatives() + DatePatterns.get_months() + ")"), False, False)
        ]

    @staticmethod
    def get_months_by_calendar():
        return {'דצמבר': 12, 'נובמבר': 11, 'אוקטובר': 10, 'ספטמבר': 9,
                'אוגוסט': 8, 'יולי': 7, 'יוני': 6, 'מאי': 5,
                'אפריל': 4, 'מרץ': 3, 'פברואר': 2, 'ינואר': 1}

    @staticmethod
    def get_relatives():
        b = get_hex_unicode("ב")
        m = get_hex_unicode("מ")
        l = get_hex_unicode("ל")
        h = get_hex_unicode("ה")
        makaf = "-"
        relatives = [b, m, l, h, makaf]
        return "[" + ''.join(relatives) + "]?"

    @staticmethod
    def get_months():
        return "(?:" + get_hex_unicode("אוגוסט") + "|" + get_hex_unicode("נובמבר") + ")"


class DatePattern:
    def __init__(self, name, pattern, with_year, is_range):
        self.name: str = name
        self.pattern: str = pattern
        self.with_year: bool = with_year
        self.is_range: bool = is_range


class DateSeperator(Enum):
    DOT = 1
    SLASH = 2
    BACKSLASH = 3


def complete_year_by_time_stamp(date, post_time, seperator):
    date = f'{date}{seperator}{post_time.year}'
    date = dparser.parse(date, fuzzy=True, dayfirst=True).date()
    while date < post_time:
        date = datetime.date(date.year + 1, date.month, date.day)
    return date


class DateReg:
    def __init__(self, date, date_pattern):
        self.date: str = date
        self.date_pattern: DatePattern = date_pattern
        self.with_dots: DateSeperator = self.init_seperator()

    def init_seperator(self):
        if '/' in self.date:
            return DateSeperator.SLASH
        elif '\\' in self.date:
            return DateSeperator.BACKSLASH
        else:
            return DateSeperator.DOT

    def get_seperator(self):
        if self.with_dots == DateSeperator.SLASH:
            return '/'
        elif self.with_dots == DateSeperator.BACKSLASH:
            return '\\'
        else:
            return '.'

    def complete_year(self, post_time):
        if not self.date_pattern.with_year:
            self.date = complete_year_by_time_stamp(self.date, post_time, self.get_seperator())

    def hebrew_to_calendar(self):
        if self.date_pattern.name == "part_date_half_hebrew_pattern":
            date = self.date.split()
            month_to_calendar = DatePatterns.get_months_by_calendar()
            if not date[1] in month_to_calendar:  # relative char before month
                date[1] = date[1][1:]
            assert date[1] in month_to_calendar
            self.date = date[0] + self.get_seperator() + str(month_to_calendar[date[1]])

    def range_to_dates(self, post_time):
        try:
            start_date, end_date = self.date.split('-')
            end_date = complete_year_by_time_stamp(end_date, post_time, self.get_seperator())
            if self.date_pattern.name == 'combined_full_start_end_pattern4':
                return self.fill_year_from_start_date_and_range_to_dates(end_date, start_date)  # TODO [AA] : re-exam
            splitted_start_date = start_date.split(self.get_seperator())
            if len(splitted_start_date) <= 1:  # DD only
                start_date = start_date + self.get_seperator() + str(end_date.month)
            if len(splitted_start_date) <= 2:  # DD/MM
                start_date = start_date + self.get_seperator() + str(end_date.year)
            start_date = dparser.parse(start_date, fuzzy=True, dayfirst=True).date()
            return start_date, end_date
        except dateutil.parser._parser.ParserError:
            return '', ''

    def fill_year_from_start_date_and_range_to_dates(self, end_date, start_date):
        start_date = dparser.parse(start_date, fuzzy=True, dayfirst=True).date()
        expected_end_date = datetime.date(start_date.year, end_date.month, end_date.day)
        if expected_end_date < start_date:
            expected_end_date = datetime.date(start_date.year + 1, end_date.month, end_date.day)
        return start_date, expected_end_date
