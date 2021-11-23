import dateutil
import dateutil.parser as dparser


# Hebrew -> hex unicode
def get_hex_unicode(reg_str):
    uni_str = ''
    for letter in reg_str:
        uni_str += r'\u0'
        uni_str += f'{hex(ord(letter)).split("x")[1]}'
    return uni_str


class DatePatterns:
    def __init__(self):
        self.patterns = [
            DatePattern("combined_full_start_end_pattern1", "\d+[-]\d+[/.]\d+[/.]\d+", True, True),  # DD-DD/MM/YY
            DatePattern("combined_full_start_end_pattern2", "\d+[/.]\d+[/.]\d+[-]\d+[/.]\d+[/.]\d+", True, True),
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


class DateReg:
    def __init__(self, date, date_pattern, with_dots):
        self.date: str = date
        self.date_pattern: DatePattern = date_pattern
        self.with_dots: bool = with_dots

    def get_seperator(self):
        return '.' if self.with_dots else '/'

    def manipulate(self):
        self.hebrew_to_calendar()
        self.complete_year()

    def complete_year(self):
        if not self.date_pattern.with_year:
            self.date = f'{self.date}{self.get_seperator()}21'  # TODO [AA] : change 2021 to good year

    def hebrew_to_calendar(self):
        if self.date_pattern.name == "part_date_half_hebrew_pattern":
            date = self.date.split()
            month_to_calendar = DatePatterns.get_months_by_calendar()
            if not date[1] in month_to_calendar:  # relative char before month
                date[1] = date[1][1:]
            assert date[1] in month_to_calendar
            self.date = date[0] + self.get_seperator() + str(month_to_calendar[date[1]])

    def range_to_dates(self):
        try:
            start_date, end_date = self.date.split('-')
            if self.date_pattern.name == 'combined_full_start_end_pattern4':
                return self.fill_year_from_start_date_and_range_to_dates(end_date, start_date)
            end_date = dparser.parse(end_date, fuzzy=True, dayfirst=True).date()
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
        expected_end_date = end_date + self.get_seperator() + str(start_date.year)
        expected_end_date = dparser.parse(end_date, fuzzy=True, dayfirst=True).date()
        if expected_end_date < start_date:
            end_date = end_date + self.get_seperator() + str(start_date.year + 1)
            return start_date, dparser.parse(end_date, fuzzy=True, dayfirst=True).date()
        return start_date, expected_end_date
