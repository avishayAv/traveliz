import datetime
import difflib
import json
import re
import dateutil.parser as dparser
from DateParser import DatePatterns, DateReg

from FacebookGroup import FacebookGroups

def searching_for_sublet(title, text):
    pattern = 'מחפש'
    return bool(re.findall(pattern, title + text))


def parse_phone_number(title, text):
    phones = []
    text = title + text
    text.replace('+972', '0')
    pattern = r'\d{3}-?[0-9]+-?[0-9]+-?[0-9]+'
    for match in re.findall(pattern, text):
        phones.append(match)
    return phones


def parse_price(title, text) -> (str, int):
    pattern = r'\s\d{1},?\d{2,3}\s'
    text = title + text
    text = re.sub("\s+", " ", text)
    words = text.split()
    prices = {}
    for i, match in enumerate(re.findall(pattern, text)):

        cleaned_match = re.findall(r'\d{1},?\d{2,3}', match)[0]
        match_index = words.index(cleaned_match)
        # todo: analyze next and prev word
        price = int(cleaned_match.replace(',', ''))
        if price not in prices.values():
            prices[f'price_{i}'] = price
    return prices


def parse_location(title, text, group_id, locations_json_path='israel_cities.json'):
    def clean_and_match(sub_text, decrease=0.0, similarity_th=0.85):
        res = match(sub_text, similarity_th, decrease=0 + decrease)
        if sub_text.startswith('ב'):
            res += match(sub_text[1:], similarity_th, decrease=0.05 + decrease)
        return res

    def match(sub_text, similarity_th=0.85, decrease=0.0):
        res = []
        for place in israel_cities:

            similarity = difflib.SequenceMatcher(None, place, sub_text).ratio() - decrease

            if similarity > similarity_th:
                res.append((place, similarity))
        return res

    fb_groups = FacebookGroups().groups
    optional_places = [x.location for x in fb_groups if x.group_id == group_id and x.location is not None]
    if len(optional_places) > 0:
        assert len(optional_places) == 1
        return optional_places[0]
    israel_cities = json.load(open(locations_json_path, encoding='utf8')) # TODO [YG] : this kind of things should be static (happen once)
    israel_cities = [x['name'] for x in israel_cities]
    words = re.findall(r'\w+', title + text)
    optional_places = []
    prev_word = ''
    for word in words:
        optional_places.extend(clean_and_match(word, decrease=0.05 if prev_word == 'ליד' else 0.0))
        prev_word = word
    for word1, word2 in zip(words[:-1], words[1:]):
        optional_places.extend(clean_and_match(' '.join([word1, word2]), decrease=0.05 if prev_word == 'ליד' else 0.0))
        prev_word = word1
    if not optional_places:
        return None
    ret = sorted(optional_places, key=lambda x: x[1], reverse=True)[0]
    return ret[0]


# do not use datefinder - not working well with hebrew
# TODO [AA] : return value should be list(start,end) and not just (start,end) - in case of multiple date options
# TODO [AA] : think about grepping other fields. maybe title if exist?
def extract_dates_from_text(text):
    dates = []
    for date_pattern in DatePatterns().patterns:
        dates_regex = [DateReg(x, date_pattern, "." in x) for x in re.findall(date_pattern.pattern, text)]
        for date_regex in dates_regex:
            date_regex.complete_year()
        dates.extend(dates_regex)
        if (date_pattern.name.startswith('combined') and len(dates) >= 1) or len(dates) >= 2:
            break

    if len(dates) == 0:     # TODO [AA] : handle empty case
        return None, None

    # Prioritize ranged dates
    range_dates = [d for d in dates if d.date_pattern.is_range]
    if len(range_dates) > 0:
        range_date = range_dates[0] # TODO [AA] : handle multiple ranges
        return range_date.range_to_dates()

    real_dates = [dparser.parse(i.date, fuzzy=True, dayfirst=True).date() for i in dates]
    return min(real_dates), max(real_dates)
