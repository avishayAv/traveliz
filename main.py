from facebook_scraper import get_posts
import pickle
import datetime
from tqdm import tqdm
from Sublet import Sublet, Airbnb, Facebook
import time
from FacebookGroup import FacebookGroups
import random
import os
import json
from AirbnbUtils import AirbnbParser, AirbnbScraper
from ParsingFunctions import *
import numpy as np
from whatsapp_utils import download_data_from_groups
from data_utils.tagging_utils import create_excel_for_tagging_data


def get_data_from_facebook(already_done):
    fb_groups = FacebookGroups().groups
    fb_groups_list_private = [group.group_id for group in fb_groups if not group.is_public]
    fb_groups_list_public = [group.group_id for group in fb_groups if group.is_public]
    credentials = [('avishaya67@gmail.com', '0528773202'), ('yishayahug@mail.tau.ac.il', 'w,+L<e8VjmJ+,6Y')]
    for fb_group in fb_groups_list_private:
        if fb_group not in already_done:
            group_posts = []
            for post in get_posts(group=fb_group, pages=random.randint(2, 6), credentials=random.choice(credentials),
                                  options={"progress": True, "posts_per_page": random.randint(50,
                                                                                              100)}):  # TODO : change number of pages and posts per page + add comments?
                group_posts.append(post)
            yield fb_group, group_posts
            time.sleep(random.randint(0, 200))
    for fb_group in fb_groups_list_public:
        if fb_group not in already_done:
            group_posts = []
            for post in get_posts(group=fb_group, pages=random.randint(1, 2), credentials=random.choice(credentials),
                                  options={"progress": True, "posts_per_page": random.randint(50,
                                                                                              100)}):  # TODO : change number of pages and posts per page + add comments?
                group_posts.append(post)
            yield fb_group, group_posts
            time.sleep(random.randint(0, 200))


def parse_data_from_facebook(dict_of_sublets):
    list_of_sublets = []
    for group_id, posts in dict_of_sublets.items():
        for post in posts:
            list_of_sublets.append((group_id, post))
    sublets = []
    parse_location = ParseLocation()
    for group_id, sublet in tqdm(list_of_sublets):
        post_title = sublet.get('title', '')
        post_text = sublet.get('text')
        if searching_for_sublet(post_title, post_text):
            continue

        assert post_text is not None
        post_url = sublet['post_url']
        post_time = sublet['time']
        end_date, rooms, start_date = parse_rooms_and_dates_from_facebook(post_text, post_time)
        location = parse_location(post_title, post_text, group_id,
                                  listing_location=sublet['listing_location'] if 'listing_location' in sublet else None)
        phones, masked_text = parse_phone_number(post_title, post_text)
        prices = parse_price(masked_text, listing_price=sublet['listing_price'] if 'listing_price' in sublet else None)
        max_people = 0  # TODO : parse max_people from text

        images = sublet['images']
        sublets.append(
            Facebook(post_url, location, prices, max_people, images, rooms,
                     post_time, start_date, end_date, phones))
    return sublets


def parse_rooms_and_dates_from_facebook(post_text, post_time):
    rooms, masked_text = extract_rooms_from_text(post_text)
    start_date, end_date = extract_dates_from_text(masked_text, post_time)
    return end_date, rooms, start_date


def facebook():
    dict_of_sublets = pickle.load(open("dict_of_sublets.p", 'rb')) if os.path.exists("dict_of_sublets.p") else {}
    # for group_id, group_posts in tqdm(get_data_from_facebook(already_done=set(dict_of_sublets.keys())),
    #                                   desc='extracting groups data'):
    #     dict_of_sublets[group_id] = group_posts
    #     pickle.dump(dict_of_sublets, open('dict_of_sublets.p', 'wb'))
    return parse_data_from_facebook(dict_of_sublets)


def parse_data_from_whatsapp(data):
    parse_location = ParseLocation()
    group_to_location = {'סאבלט בדפנה': 'דפנה'}
    for group_name, messages_per_date in data.items():
        for date1, messages in messages_per_date.items():
            for message in messages:
                # TODO [YG + AA] : parse common fields together with facebook
                # TODO [YG] : parse images by phone number
                post_time = datetime.datetime.strptime(date1 + '/' + message['time'], '%m/%d/%Y/%I:%M %p')
                price = parse_price(message['text'], None, None)
                location = parse_location(text=message['text'], title=None, group_id=None,
                                          listing_location=group_to_location[group_name])
                phone = message['sender']


def whatsapp():
    groups = ['סאבלט בדפנה']
    data = download_data_from_groups(groups)
    parse_data_from_whatsapp(data)


def main():
    # parser = AirbnbParser()
    # res = parser.parse_airbnb_data(json_file_path = "airbnb_data/jlm.json")
    # scraper = AirbnbScraper()
    # scraper.airbnb_scraper()
    #airbnb_listings = airbnb_read_data_from_json()
    # sublets = []
    # ws['A1'] = a[2]['text']
    create_excel_for_tagging_data()
    #posts_dict = read_excel_end_create_dict_of_tagged_data(name="facebook_posts_1")
    y = 5
    # excel_data_df = pd.read_excel('/Users/eliyasegev/Desktop/Tagged_data.xlsx', sheet_name='Facebook_data')
    # for column in excel_data_df.columns.ravel():
    # print(column, ": " + str(excel_data_df[column].tolist()))

    # sublets.extend(facebook())
    pass


if __name__ == "__main__":
    main()
