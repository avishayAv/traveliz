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


def parse_price(title, text, listing_price):
    def get_symbol(word):
        shekel_pattern = r'₪|שקל|ils|ש"ח'
        dollar_pattern = r'\$|דולר|Dollar'
        for pat in [shekel_pattern, dollar_pattern]:
            if len(re.findall(pat, word)) > 0:
                return pat[0]
        return False

    def find_description(word):
        return word.replace(',', '')

    pattern = r'\D[1-9],?\d{2,3}\D'
    meter_pattern = r'מ"ר|מר|מטר'
    if listing_price is not None:
        text = listing_price
    else:
        text = title + text
    text = re.sub("\s+|\(|\)", " ", text)
    text = re.sub("\+972", "0", text)
    text = re.sub("2021", "", text)
    text = re.sub("2022", "", text)
    for match in re.finditer(r"\D\d{3,4}-\d{3,4}\D", text):
        text = text[:match.start()] + text[match.start():match.end()].replace('-','  ') + text[match.end():]
    words = text.split() + ['', '']  # avoid index error
    prices = {}
    price_to_symbol = {}
    for i, match in enumerate(re.findall(pattern, text)):
        # clean match from spaces
        match = re.sub("\s+", "", match)
        match_index = [i for i in range(len(words)) if match in words[i]]
        match_index = match_index[0]

        cleaned_match = re.findall(r'\d{1},?\d{2,3}', match)[0]
        price = int(cleaned_match.replace(',', ''))
        next_word = words[match_index + 1]
        symbol = get_symbol(next_word)

        if symbol:
            next_word = words[match_index + 2]
            price_to_symbol[price] = symbol
        else:
            if len(re.findall(meter_pattern, next_word)) > 0:
                continue
        if price not in prices.values():
            description = find_description(next_word)
            prices[f'price_{i}_{description}'] = price

    return {k: (v, price_to_symbol.get(v, '₪')) for k, v in sorted(prices.items(), key=lambda x: x[1])}


class ParseLocation:
    def __init__(self):
        israel_cities = json.load(open('israel_cities.json', encoding='utf8'))
        self.israel_cities_names = [(x['name'], x['english_name']) for x in israel_cities]
        israel_postal = json.load(open('israel_postal.json', encoding='utf8'))
        self.zip_code_to_location = {}
        for dict1 in israel_postal:
            if 'zip' not in dict1:
                continue
            zip1 = str(dict1['zip'])[0:5]
            location = dict1['n']
            self.zip_code_to_location[zip1] = location

    def __call__(self, title, text, group_id, listing_location):
        def clean_and_match(sub_text, decrease=0.0, similarity_th=0.85):
            res = match(sub_text, similarity_th, decrease=0 + decrease)
            if sub_text.startswith('ב'):
                res += match(sub_text[1:], similarity_th, decrease=-0.05 + decrease)
            return res

        def match(sub_text, similarity_th=0.85, decrease=0.0):
            res = []
            for place in self.israel_cities_names:
                place, place_in_english = place
                similarity = difflib.SequenceMatcher(None, place, sub_text).ratio() - decrease
                if similarity > similarity_th:
                    res.append((place, similarity))
                if sub_text.isalpha():
                    similarity = difflib.SequenceMatcher(None, place_in_english, sub_text).ratio() - decrease
                    if similarity > similarity_th:
                        res.append((place, similarity))
            return res

        # extract location from group name
        fb_groups = FacebookGroups().groups
        optional_places = [x.location for x in fb_groups if x.group_id == group_id and x.location is not None]
        if len(optional_places) > 0:
            assert len(optional_places) == 1
            return optional_places[0]

        # extract location from listing location field in facebook

        if listing_location is not None:
            if listing_location.isnumeric():
                if listing_location in self.zip_code_to_location:
                    return self.zip_code_to_location[listing_location]
            else:
                places = clean_and_match(listing_location.casefold(), decrease=0.0)
                if places:
                    assert len(places) == 1
                    return places[0][0]

        words = re.findall(r'\w+', title + text)
        # extract from text
        optional_places = []
        prev_word = ''
        for word in words:
            optional_places.extend(clean_and_match(word, decrease=0.05 if prev_word == 'ליד' else 0.0))
            prev_word = word
        for word1, word2 in zip(words[:-1], words[1:]):
            optional_places.extend(
                clean_and_match(' '.join([word1, word2]), decrease=0.05 if prev_word == 'ליד' else 0.0))
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

    if len(dates) == 0:  # TODO [AA] : handle empty case
        return None, None

    # Prioritize ranged dates
    range_dates = [d for d in dates if d.date_pattern.is_range]
    if len(range_dates) > 0:
        range_date = range_dates[0]  # TODO [AA] : handle multiple ranges
        return range_date.range_to_dates()

    real_dates = [dparser.parse(i.date, fuzzy=True, dayfirst=True).date() for i in dates]
    return min(real_dates), max(real_dates)
