import dateutil
import dateutil.parser as dparser

class DatePatterns:
    def __init__(self):
        self.patterns = [
         DatePattern("combined_full_start_end_pattern1", "\d+[-]\d+[/.]\d+[/.]\d+", True, True), # DD-DD/MM/YY
         DatePattern("combined_full_start_end_pattern2", "\d+[/.]\d+[/.]\d+[-]\d+[/.]\d+[/.]\d+", True, True),  # DD/MM/YY-DD/MM/YY
         DatePattern("combined_full_start_end_pattern3", "\d+[/.]\d+[-]\d+[/.]\d+[/.]\d+", True, True), # DD/MM-DD/MM/YY
         DatePattern("combined_full_start_end_pattern4", "\d+[/.]\d+[/.]\d+[-]\d+[/.]\d+", True, True), # DD/MM/YY-DD/MM
         DatePattern("combined_full_start_end_pattern5", "\d+[/.]\d+[-]\d+[/.]\d+", False, True), # DD/MM-DD/MM
         DatePattern("combined_part_start_end_pattern2", "\d+[-]\d+[/.]\d+", False, True),  # D-D/M
         DatePattern("full_date_pattern", "\d+[/.]\d+[/.]\d+", True, False), # D/M/YY, D/M/YYYY, DD/M/YY, DD/M/YYYY, D/MM/YY, D/MM/YYYY, DD/MM/YY, DD/MM/YYYY
         DatePattern("part_date_pattern", "\d+[/.]\d+", False, False)  # D/M, DD/M, D/MM, DD/MM
                         ]


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

    def complete_year(self):
        if not self.date_pattern.with_year:
            self.date = f'{self.date}{self.get_seperator()}22'  # TODO [AA] : change 2022 to good year


    def range_to_dates(self):
        try:
            start_date, end_date = self.date.split('-')
            if self.date_pattern.name == 'combined_full_start_end_pattern4':
                return self.fill_year_from_start_date_and_range_to_dates(end_date, start_date)
            end_date = dparser.parse(end_date, fuzzy=True, dayfirst=True).date()
            splitted_start_date = start_date.split(self.get_seperator())
            if len(splitted_start_date) <= 1: # DD only
                start_date = start_date + self.get_seperator() + str(end_date.month)
            if len(splitted_start_date) <= 2: # DD/MM
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
            end_date = end_date + self.get_seperator() + str(start_date.year+1)
            return start_date, dparser.parse(end_date, fuzzy=True, dayfirst=True).date()
        return start_date, expected_end_date



