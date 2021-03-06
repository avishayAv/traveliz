import datetime
import difflib
import json
import re

from currency_converter import CurrencyConverter

from DateParser import DatePatterns, DateReg
from FacebookGroup import FacebookGroups
from HyperParams import get_location_hyper_params
from PriceParser import PriceParser
from RoomsParser import RoomsParser
from Sublet import Rooms, Location, Price
from paths import REPOSITORY_ROOT
from utils import remove_time_stamp_from_text, get_hebrew_to_real_number, main_locations_to_cities


# TODO [AA + YG] : refactor + standartize

def searching_for_sublet(title, text):
    pattern = 'מחפש'
    return bool(re.findall(pattern, title + text))


def parse_phone_number(title, text):
    phones = set()
    if title is None:
        title = ''
    text = title + text
    pattern1 = r'0\d{2}-?[0-9]+-?[0-9]+-?[0-9]+'
    pattern2 = r'972\d{2}-?[0-9]+-?[0-9]+-?[0-9]+'
    masked_text = text
    for match in list(re.finditer(pattern1, text)) + list(re.finditer(pattern2, text)):

        if (match.start() - 1 >= 0 and text[match.start() - 1].isnumeric()) or (
                match.end() < len(text) and text[match.end()].isnumeric()):
            continue
        phone_num = text[match.start():match.end()].replace('972', '0').replace('-', '')
        if 9 <= len(phone_num) <= 10:
            phones.add(phone_num)
        # TODO [YG]: bug need to be fixed
        masked_text = text[:match.start()] + text[match.end():]

    return phones, masked_text


def parse_price(text, listing_price, city, shared_apt, period):
    def get_symbol(word):
        shekel_pattern = r'₪|שקל|ils|ש"ח|NIS|שקלים'
        dollar_pattern = r'\$|דולר|Dollar'
        for pat in [shekel_pattern, dollar_pattern]:
            if len(re.findall(pat, word)) > 0:
                return pat[0]
        return False

    converter = CurrencyConverter()
    period = period.days if period else None
    price_parser = PriceParser()
    pattern = price_parser.price_pattern
    meter_pattern = price_parser.meter_pattern
    if listing_price is not None:
        text = listing_price
    text = re.sub(r"\s+|\(|\)", " ", text)
    for i in [-1, 0, 1]:
        year = str(int(datetime.date.today().year) + i)
        text = re.sub(year, "", text)
    text += ' '

    final_price = Price()
    for i, match in enumerate(re.finditer(pattern, text)):
        if match.end() == len(text):
            next_words = ['', '']
        else:
            next_words = text[match.end():].split() + ['']
        prev_words = " ".join(text[:match.start()].split()[-2:])
        match = text[match.start():match.end()]
        # clean match from spaces
        match = re.sub(r"\D+", "", match)
        price = int(match.replace(',', ''))

        next_word = next_words[0]
        if len(re.findall(meter_pattern, next_word)) > 0:
            continue

        symbol = get_symbol(next_word)
        if symbol:
            if symbol == '$':
                price = converter.convert(price, 'USD', 'ILS')
            next_words = next_words[1:]

        next_words = " ".join(next_words[:4])
        final_price.set_price(prev_words + " " + next_words, price, city, shared_apt, period)

    return final_price


class ParseLocation:
    def __init__(self):

        israel_cities = json.load(open(REPOSITORY_ROOT / 'israel_cities.json', encoding='utf8'))
        self.israel_cities_names = [(x['name'], x['english_name']) for x in israel_cities]
        self.city_to_streets = json.load(open(REPOSITORY_ROOT / 'city_to_streets.json'))
        self.main_locations_to_cities = main_locations_to_cities
        israel_postal = json.load(open(REPOSITORY_ROOT / 'israel_postal.json', encoding='utf8'))
        self.zip_code_to_location = {}
        for dict1 in israel_postal:
            if 'zip' not in dict1:
                continue
            zip1 = str(dict1['zip'])[0:5]
            location = dict1['n']
            self.zip_code_to_location[zip1] = location

    def clean_and_match(self, sub_text, city=None, decrease=0.0, similarity_th=get_location_hyper_params.similarity_th):
        res = self.match(sub_text, city, similarity_th, decrease=0 + decrease)
        # TODO [YG]: extract hyper-params to different file
        if sub_text.startswith('ב'):
            res += self.match(sub_text[1:], city, similarity_th, decrease=-0.03 + decrease)
        elif sub_text.startswith('שב'):
            res += self.match(sub_text[1:], city, similarity_th, decrease=-0.07 + decrease)
        if sub_text in self.main_locations_to_cities:
            res += [(self.main_locations_to_cities[sub_text], 0.95)]
        if sub_text.startswith('מ') and sub_text[1:] in self.main_locations_to_cities:
            res += [(self.main_locations_to_cities[sub_text[1:]], 0.90)]
        return res

    def match(self, sub_text, city, similarity_th=0.85, decrease=0.0):
        res = []
        places_in_israel = self.israel_cities_names if city is None else self.city_to_streets[city]
        for place in places_in_israel:
            if type(place) is tuple:
                assert len(place) == 2
                place, place_in_english = place
            else:
                place, place_in_english = place, ''
            if place == sub_text:
                similarity = 1 - decrease

                if place == 'תל אביב':
                    similarity += get_location_hyper_params.tel_aviv_priority
            else:
                similarity = 0
            if similarity > similarity_th:
                res.append((place, similarity))
            if sub_text.isalpha():
                similarity = difflib.SequenceMatcher(None, place_in_english, sub_text).ratio() - decrease
                if similarity > similarity_th:
                    res.append((place, similarity))
        return res

    def get_city(self, words, group_id, listing_location):
        optional_places = []
        # extract location from group name
        if group_id is not None:
            fb_groups = FacebookGroups().groups
            optional_places += [(x.location, 0.99) for x in fb_groups if
                                x.group_id == group_id and x.location is not None]

        # extract location from listing location field in facebook
        if listing_location is not None:
            if listing_location.isnumeric():
                if listing_location in self.zip_code_to_location:
                    return self.zip_code_to_location[listing_location]
            else:
                optional_places += self.clean_and_match(listing_location.casefold(), city=None, decrease=0.05)
        prev_word = ''
        for word in words:
            if 'רחוב' not in prev_word and 'שדרות' not in prev_word:
                optional_places.extend(self.clean_and_match(word, city=None,
                                                            decrease=get_location_hyper_params.prev_word_decrease if prev_word == 'ליד' else 0.0))
            prev_word = word
        prev_word = ''
        for word1, word2 in zip(words[:-1], words[1:]):
            if 'רחוב' not in prev_word and 'שדרות' not in prev_word:
                optional_places.extend(
                    self.clean_and_match(' '.join([word1, word2]), city=None,
                                         decrease=get_location_hyper_params.prev_word_decrease if prev_word == 'ליד' else 0.0))
            prev_word = word1
        if not optional_places:
            return None
        ret = sorted(optional_places, key=lambda x: x[1], reverse=True)[0]
        return ret[0]

    def get_street(self, words, city):
        # TODO [YG]: extract to function
        prev_word = ''
        optional_places = []
        for word in words:
            dec = get_location_hyper_params.prev_word_street_decreas if 'רחוב' in prev_word or 'שדרות' in prev_word else 0
            optional_places.extend(self.clean_and_match(word, city=city,
                                                        decrease=dec))
            prev_word = word
        prev_word = ''
        for word1, word2 in zip(words[:-1], words[1:]):
            dec = get_location_hyper_params.prev_word_street_decreas if 'רחוב' in prev_word or 'שדרות' in prev_word else 0
            optional_places.extend(
                self.clean_and_match(' '.join([word1, word2]), city=city,
                                     decrease=dec))
            prev_word = word1
        if not optional_places:
            return None
        ret = sorted(optional_places, key=lambda x: x[1], reverse=True)[0]
        return ret[0]

        # extract from text

    def __call__(self, title, text, group_id, listing_location):
        if title is None:
            title = ''
        words = re.findall(r'\w+', title + text)
        city = self.get_city(words, group_id, listing_location)
        street = None
        # TODO [YG]: extract
        if city in ['תל אביב', 'ירושלים', 'חיפה']:
            street = self.get_street(words, city)
        return Location(city=city, street=street)


# do not use datefinder - not working well with hebrew
# TODO [AA] : think about grepping other fields. maybe title if exist?
def extract_dates_from_text(text, post_time):
    post_time = post_time.date() if isinstance(post_time, datetime.datetime) else post_time  # TODO [AA] : make one-flow
    dates = []
    for date_pattern in DatePatterns().patterns:
        dates_regex = [DateReg(x, date_pattern) for x in re.findall(date_pattern.pattern, text)]
        for date_regex in dates_regex:
            date_regex.hebrew_to_calendar()
        dates.extend(dates_regex)
        if (date_pattern.name.startswith('combined') and len(dates) >= 1) or len(dates) >= 2:
            break

    if len(dates) == 0:
        return None, None

    # Prioritize ranged dates
    range_dates = [d for d in dates if d.date_pattern.is_range]
    if len(range_dates) > 0:
        range_date = range_dates[0]  # TODO [AA] : handle multiple ranges
        return range_date.range_to_dates(post_time)

    for date in dates:
        date.str_to_date(post_time)
    dates = [inst.date for inst in dates]
    if len(dates) == 1:
        return dates[0], None
    return min(dates), max(dates)


def try_room_pattern_and_cleanup_text(room_pattern, text, convert_from_hebrew=False, living_room=None,
                                      half_included=False, no_number=False, roommates=False):
    hebrew_to_real_number = get_hebrew_to_real_number()
    grep_rooms = re.findall(room_pattern, text)
    living_room_exist = re.findall(living_room, text) if living_room else None
    if len(grep_rooms) > 0:
        if no_number:  # single bed room pattern
            grep_rooms = [(1, 'bedroom')]
        rooms = Rooms()
        rooms.shared = roommates
        rooms.number = float(hebrew_to_real_number[grep_rooms[0][0]]) if convert_from_hebrew else float(
            grep_rooms[0][0])
        rooms.number = rooms.number + 1 if living_room_exist else rooms.number
        rooms.number = rooms.number + 0.5 if half_included else rooms.number
        masked_text = re.sub(room_pattern, '', text)
        return rooms, masked_text
    return None, None


def extract_rooms_from_text(text):
    rooms_parser = RoomsParser()

    rooms, masked_text = try_room_pattern_and_cleanup_text(rooms_parser.total_rooms, text)
    if rooms is not None:
        return rooms, masked_text

    rooms, masked_text = try_room_pattern_and_cleanup_text(rooms_parser.hebrew_total_rooms, text, True)
    if rooms is not None:
        return rooms, masked_text

    rooms, masked_text = try_room_pattern_and_cleanup_text(rooms_parser.hebrew_total_rooms_w_half, text,
                                                           True, half_included=True)
    if rooms is not None:
        return rooms, masked_text

    rooms, masked_text = try_room_pattern_and_cleanup_text(rooms_parser.bed_rooms, text, False,
                                                           rooms_parser.living_room)
    if rooms is not None:
        return rooms, masked_text

    rooms, masked_text = try_room_pattern_and_cleanup_text(rooms_parser.hebrew_bed_rooms, text, True,
                                                           rooms_parser.living_room)
    if rooms is not None:
        return rooms, masked_text

    rooms, masked_text = try_room_pattern_and_cleanup_text(rooms_parser.shared_apt_w_rooms, text, False,
                                                           rooms_parser.living_room, roommates=True)
    if rooms is not None:
        return rooms, masked_text

    rooms, masked_text = try_room_pattern_and_cleanup_text(rooms_parser.shared_apt_w_rooms_hebrew, text, True,
                                                           rooms_parser.living_room, roommates=True)
    if rooms is not None:
        return rooms, masked_text

    rooms, masked_text = try_room_pattern_and_cleanup_text(rooms_parser.single_bed_room, text, False,
                                                           rooms_parser.living_room, no_number=True)
    if rooms is not None:
        return rooms, masked_text

    rooms = Rooms()
    one_room_shared_apt = re.findall(rooms_parser.shared_apt, text)
    if len(one_room_shared_apt) > 0:
        rooms.number = 1
        rooms.shared = True
        return rooms, text

    one_room_apt = re.findall(rooms_parser.one_room_apt, text)
    rooms.number = float(1) if len(one_room_apt) > 0 else None
    return rooms, text


class FreeTextParser:
    def __init__(self):
        self.parse_location = ParseLocation()

    def parse_free_text_to_md(self, post_title='', post_text='', post_time=None, listing_location=None, group_id=None,
                              listing_price=None):
        post_text = remove_time_stamp_from_text(post_text)
        rooms, masked_text = extract_rooms_from_text(post_text)
        start_date, end_date = extract_dates_from_text(masked_text, post_time)
        location = self.parse_location(post_title, post_text, group_id,
                                       listing_location=listing_location)
        phones, masked_text = parse_phone_number(post_title, post_text)
        period = None if start_date is None or end_date is None else end_date - start_date
        prices = parse_price(masked_text, listing_price=listing_price, city=location.city, shared_apt=rooms.shared,
                             period=period)
        max_people = 0  # TODO : parse max_people from text
        return start_date, end_date, rooms, phones, prices, location, max_people
