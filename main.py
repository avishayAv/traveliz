import os
import pickle
import random
import time
import argparse
from datetime import datetime
from pathlib import Path

from facebook_scraper import get_posts
from tqdm import tqdm

from AirbnbUtils import AirbnbScraper, AirbnbParser

from FacebookSql import FacebookSql
from ParsingFunctions import *
from Sublet import Facebook, WhatsApp
from paths import AIRBNB_DATA_PATH, WHATSAPP_DATA_PATH, FACEBOOK_DATA_PATH
from utils import whatsapp_group_to_location
from whatsapp_utils import download_data_from_groups

def get_data_from_facebook(already_done):
    fb_groups = FacebookGroups().groups
    fb_groups_list_private = [group.group_id for group in fb_groups if not group.is_public]
    fb_groups_list_public = [group.group_id for group in fb_groups if group.is_public]
    credentials = [('yishayahug@mail.tau.ac.il', 'shaya321#@!!')]
    for fb_group in fb_groups_list_private:
        if fb_group not in already_done:
            group_posts = []
            for post in get_posts(group=fb_group, pages=random.randint(2, 6), credentials=random.choice(credentials),
                                  options={"progress": True, "posts_per_page": random.randint(5,
                                                                                              10)}):  # TODO : change number of pages and posts per page + add comments?
                group_posts.append(post)
            yield fb_group, group_posts
            time.sleep(random.randint(0, 200))
    for fb_group in fb_groups_list_public:
        if fb_group not in already_done:
            group_posts = []
            for post in get_posts(group=fb_group, pages=random.randint(1, 2), credentials=random.choice(credentials),
                                  options={"progress": True, "posts_per_page": random.randint(5,
                                                                                              10)}):  # TODO : change number of pages and posts per page + add comments?
                group_posts.append(post)
            yield fb_group, group_posts
            time.sleep(random.randint(0, 200))


def parse_data_from_facebook(dict_of_sublets):
    list_of_sublets = []
    for group_id, posts in dict_of_sublets.items():
        for post in posts:
            list_of_sublets.append((group_id, post))
    sublets = []
    parser = FreeTextParser()
    for group_id, sublet in tqdm(list_of_sublets):
        post_title = sublet.get('title', '')
        post_text = sublet.get('text')
        if searching_for_sublet(post_title, post_text):
            continue

        assert post_text is not None
        post_url = sublet['post_url']
        post_time = sublet['time'] if sublet['time'] is not None else datetime.datetime.now()
        start_date, end_date, rooms, phones, prices, location, max_people = \
            parser.parse_free_text_to_md(post_text=post_text, post_time=post_time,
                                         listing_location=sublet[
                                             'listing_location'] if 'listing_location' in sublet else None
                                         , group_id=group_id
                                         , listing_price=sublet['listing_price'] if 'listing_price' in sublet else None)
        images = sublet['images']
        sublets.append(
            Facebook(post_url, location, prices, max_people, images, rooms,
                     post_time, start_date, end_date, phones))
    return sublets


def parse_rooms_and_dates_from_facebook(post_text, post_time):
    rooms, masked_text = extract_rooms_from_text(post_text)
    start_date, end_date = extract_dates_from_text(masked_text, post_time)
    return end_date, rooms, start_date

def facebook(mode, data):
    # Scarping
    if mode == 'scrape':
        dict_of_sublets = {}
        # TODO [RS] : we are being blocked currently
        for group_id, group_posts in tqdm(get_data_from_facebook(already_done=set(dict_of_sublets.keys())),
                                          desc='extracting groups data'):
            dict_of_sublets[group_id] = group_posts
            pickle.dump(dict_of_sublets, open(f'{FACEBOOK_DATA_PATH}mock.pickle', 'wb'))

    else:
        # Load pre-scraped data
        sublets = load_pre_scraped_data(data, FACEBOOK_DATA_PATH)

        # Parsing
        fb_sublets = parse_data_from_facebook(sublets)

        # Dump to DB
        # TODO [RS] : change from AWS to new our new A2 DB
        FacebookSql().dump_to_facebook_raw(fb_sublets)


def load_pre_scraped_data(data, path):
    pickle_path = Path(data if data is not None else f'{path}mock.pickle')
    if not pickle_path.exists():
        print(f'data file does not exist : {pickle_path}')
        exit(1) # TODO [AA] : wrap in exception
    return pickle.load(open(pickle_path, 'rb'))


def parse_data_from_whatsapp(data):

    parser = FreeTextParser()
    sublets = {}
    for group_name, messages_per_date in data.items():
        if group_name not in sublets:
            sublets[group_name] = []
        for date1, messages in messages_per_date.items():
            for message in messages:
                if searching_for_sublet('', message['text']):
                    continue
                post_time = datetime.datetime.strptime(date1 + '/' + message['time'], '%m/%d/%Y/%I:%M %p').date()
                start_date, end_date, rooms, _, prices, location, max_people = parser.parse_free_text_to_md(
                    post_text=message['text'], post_time=post_time,
                    listing_location=whatsapp_group_to_location[group_name])
                phone = message['sender']
                # TODO [YG] : parse images by phone number
                sublets[group_name].append([message['text'], post_time,
                                            WhatsApp(location, prices, max_people, None, rooms, post_time, phone,
                                                     start_date, end_date)])
    return sublets

def whatsapp(mode, data):
    groups = ['סאבלט בדפנה'] # TODO [YG] : let's find some more groups
    if mode == 'scrape':
        sublets = download_data_from_groups(groups) # TODO [YG] : handle chrome versioning
        pickle.dump(sublets, open(f'{WHATSAPP_DATA_PATH}mock.pickle', 'wb'))
    else:
        # Load pre-scraped data
        sublets = load_pre_scraped_data(data, WHATSAPP_DATA_PATH)

        # Parsing
        sublets = parse_data_from_whatsapp(sublets)

        # Dump to DB
        # TODO [RS] : dump sublets tp DB
        pass


def airbnb(mode, data):
    if mode == 'scrape':
        scraper = AirbnbScraper()
        scraper.airbnb_scraper()
        # TODO [ES] : dump to json (the return value is not json right now)
    else:
        # Load pre-scraped data + Paring
        parser = AirbnbParser()
        res = parser.parse_airbnb_data(json_file_path=f'{AIRBNB_DATA_PATH}jlm.json')

        # Dump to DB
        # TODO [RS] : dump json to DB
        pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-source', action='store', required=True, choices=['whatsapp', 'facebook', 'airbnb'],
                        help='data source')
    parser.add_argument('-mode', action='store', required=True, choices=['scrape', 'parse'],
                        help='scrape data to a pickle file or parse pickle file to the DB')
    parser.add_argument('-data', action='store', required=False, help='pickle file name in case of parsing mode')
    return parser.parse_args()


def main():
    args = parse_args()
    match args.source:
        case 'whatsapp':
            whatsapp(args.mode, args.data)
        case 'facebook':
            facebook(args.mode, args.data)
        case 'airbnb':
            airbnb(args.mode, args.data)
    exit(0)



if __name__ == "__main__":
    main()
