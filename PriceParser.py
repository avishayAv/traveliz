from enum import Enum
import re
from dataclasses import dataclass

@dataclass
class Price:
    month_thresholds = {'תל אביב': 2000,
                        'חיפה': 2500}

    def __init__(self):
        self.price_per_night = None
        self.discounted_price_per_night = None
        self.discounted_period = None
        self.minimum_period = None
        self.price_per_month = None
        self.price_per_weekend = None

    def set_price(self, next_words, price, city, shared_apt, period):
        found_pattern = False
        for price_pattern in PeriodPatterns.patterns:
            if re.search(price_pattern.pattern, next_words):
                found_pattern = True
                if price_pattern.period == Period.DAY:
                    if re.search(PeriodPatterns.period_pattern.pattern, next_words):
                        self.discounted_price_per_night = price
                        self.discounted_period = period
                        break
                    else:
                        self.price_per_night = price
                elif price_pattern.period == Period.WEEK:
                    self.discounted_price_per_night = price // 7
                    self.discounted_period = 7
                elif price_pattern.period == Period.MONTH:
                    self.price_per_month = price
                elif price_pattern.period == Period.WEEKEND:
                    self.price_per_weekend = price
                elif price_pattern.period == Period.PERIOD:
                    if period is not None:
                        self.discounted_price_per_night = price // period
                        self.discounted_period = period
                else:
                    self.discounted_price_per_night = price
        if not found_pattern:
            if city in self.month_thresholds and self.month_thresholds[city] < price:
                if self.price_per_month is None:
                    self.price_per_month = price
            else:
                if shared_apt:
                    if self.discounted_price_per_night is None and period is not None:
                        self.discounted_price_per_night = price // period
                        self.discounted_period = period
                else:
                    if self.price_per_night is None:
                        self.price_per_night = price


class PriceParser:
    price_pattern = r'\D[1-9]\d?,?\d{1,3}0\D'
    meter_pattern = "|".join(
        ['מגה', 'מטר', 'מר', 'מ"ר', "מ'"])


class Period(Enum):
    DAY = 1
    WEEK = 2
    MONTH = 3
    WEEKEND = 4
    PERIOD = 5


class PeriodPattern:
    def __init__(self, pattern, period: Period):
        self.pattern = pattern
        self.period = period


class PeriodPatterns:
    period_pattern = PeriodPattern(r'לתקופה|כל התקופה|לכל הימים', Period.PERIOD)

    patterns = [PeriodPattern(r'ללילה|ליום', Period.DAY),
                PeriodPattern(r'לשבוע', Period.WEEK),
                PeriodPattern(r'לחודש', Period.MONTH),
                PeriodPattern(r'לסופ"ש|לסופש|לסוף שבוע|לשישי-שבת|לשישי שבת|לשבת', Period.WEEKEND),
                period_pattern]

