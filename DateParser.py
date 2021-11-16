class DatePatterns:
    def __init__(self):
        self.patterns = [DatePattern("combined_full_start_end_pattern1", "\d+[-]\d+[/.]\d+[/.]\d+", True, True),
                         # DD-DD/MM/YY
                         DatePattern("combined_full_start_end_pattern2", "\d+[/.]\d+[/.]\d+[-]\d+[/.]\d+[/.]\d+", True,
                                     True),  # DD/MM/YY-DD/MM/YY
                         DatePattern("combined_full_start_end_pattern3", "\d+[/.]\d+[-]\d+[/.]\d+[/.]\d+", True, True),
                         # DD/MM-DD/MM/YY
                         DatePattern("combined_full_start_end_pattern4", "\d+[/.]\d+[/.]\d+[-]\d+[/.]\d+", True, True),
                         # DD/MM/YY-DD/MM
                         DatePattern("combined_full_start_end_pattern5", "\d+[/.]\d+[-]\d+[/.]\d+", False, True),
                         # DD/MM-DD/MM
                         DatePattern("combined_part_start_end_pattern2", "\d+[-]\d+[/.]\d+", False, True),  # D-D/M
                         DatePattern("full_date_pattern", "\d+[/.]\d+[/.]\d+", True, False),
                         # D/M/YY, D/M/YYYY, DD/M/YY, DD/M/YYYY, D/MM/YY, D/MM/YYYY, DD/MM/YY, DD/MM/YYYY
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

    def complete_year(self):
        if not self.date_pattern.with_year:
            return f'{self.date}{"." if self.with_dots else "/"}22'  # TODO [AA] : change 2022 to good year
