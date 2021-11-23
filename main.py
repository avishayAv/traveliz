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
from AirbnbUtils import find_airbnb_listing_location, activate_venv_command,\
    airbnb_scraper_dir_path, airbnb_data_path, list_of_locations
from ParsingFunctions import *
import numpy as np


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
        start_date, end_date = extract_dates_from_text(post_text)
        location = parse_location(post_title, post_text, group_id,listing_location=sublet['listing_location'] if 'listing_location' in sublet else None)
        rooms = 0  # TODO : parse rooms from text
        prices = parse_price(post_title,post_text,listing_price=sublet['listing_price'] if 'listing_price' in sublet else None)
        max_people = 0  # TODO : parse max_people from text
        phones = parse_phone_number(post_title, post_text)  # TODO : parse phone from text
        images = sublet['images']
        sublets.append(
            Facebook(post_url, location, prices, max_people, images, rooms,
                     post_time, start_date, end_date, phones))
    return sublets


def airbnb_scraper():
    for location in list_of_locations:
        assert len(location) == 2, f"location field is {location}, should be [<city, country>, <name of json file>]"
        get_data_from_airbnb(location=location, start_date="2021-11-25", end_date="2021-11-28",
                             number_of_pages_to_scrape=50)
        time.sleep(random.randint(120, 200))


def get_data_from_airbnb(location: list,
                         start_date: str,
                         end_date: str,
                         max_price: int = 200,  # dollars
                         min_price: int = 100,
                         number_of_pages_to_scrape: int = 8):
    command = 'scrapy crawl airbnb ' \
              '-a query="' + location[0] + '"' + \
              ' -a checkin=' + start_date + \
              ' -a checkout=' + end_date + \
              ' -a max_price=' + str(max_price) + \
              ' -a min_price=' + str(min_price) \
              + ' -o ' + location[1] + '.json ' \
                                       '-s CLOSESPIDER_PAGECOUNT=' + str(number_of_pages_to_scrape)

    os.system('( ' + activate_venv_command + ' && cd ' + airbnb_scraper_dir_path + ' && `' + command + '`)')


def airbnb_read_data_from_json():
    listings = []
    for location in list_of_locations:
        airbnb_data = parse_airbnb_data(airbnb_data_path + location[1] + ".json")
        listings.extend(airbnb_data)
    return listings


def parse_airbnb_data(json_file_path: str):
    airbnb_data = json.load(open(json_file_path, "rb"))
    airbnb_listings = []
    for listing in airbnb_data:
        name = listing['name']
        post_url = listing['url']
        area = json_file_path.split('/')[-1].split(".")[0]
        location = " ".join([find_airbnb_listing_location(listing["longitude"], listing["latitude"])+',', area])
        description = listing['description']
        rating = listing['rating_value']
        reviews = listing['reviews']
        images = listing['photos']
        amenities = listing['amenities']
        max_people = listing['person_capacity']
        prices = listing['price_rate']
        rooms = listing["bedrooms"]# if listing["bedrooms"] != 0 else None,
        bathrooms = listing["bathrooms"]# if listing["bathrooms"] != 0 else None,
        beds = listing["beds"]# if listing["beds"] != 0 else None,
        airbnb_listings.append(
            Airbnb(post_url, location, prices, max_people, images, rooms,
                   name, description, rating, reviews, amenities, bathrooms, beds))
    return airbnb_listings


def facebook():
    dict_of_sublets = pickle.load(open("dict_of_sublets.p", 'rb')) if os.path.exists("dict_of_sublets.p") else {}
    # for group_id, group_posts in tqdm(get_data_from_facebook(already_done=set(dict_of_sublets.keys())),
    #                                   desc='extracting groups data'):
    #     dict_of_sublets[group_id] = group_posts
    #     pickle.dump(dict_of_sublets, open('dict_of_sublets.p', 'wb'))
    return parse_data_from_facebook(dict_of_sublets)


def main():
    # airbnb_scraper()
    airbnb_listings = airbnb_read_data_from_json()
    sublets = []
    sublets.extend(facebook())
    pass


if __name__ == "__main__":
    main()
