import os
import pickle
import random
import time

from facebook_scraper import get_posts
from tqdm import tqdm

from AirbnbUtils import find_airbnb_listing_location, activate_venv_command, \
    airbnb_scraper_dir_path, airbnb_data_path, list_of_locations
from ParsingFunctions import *
from Sublet import Airbnb, Facebook, WhatsApp
from whatsapp_utils import download_data_from_groups


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
    parser = FreeTextParser()
    for group_id, sublet in tqdm(list_of_sublets):
        post_title = sublet.get('title', '')
        post_text = sublet.get('text')
        if searching_for_sublet(post_title, post_text):
            continue

        assert post_text is not None
        post_url = sublet['post_url']
        post_time = sublet['time']
        start_date, end_date, rooms, phones, prices, location, max_people = \
            parser.parse_free_text_to_md(post_text, post_time,
                                         listing_location=sublet[
                                             'listing_location'] if 'listing_location' in sublet else None
                                         , group_id=group_id
                                         , listing_price=sublet['listing_price'] if 'listing_price' in sublet else None)
        images = sublet['images']
        sublets.append(
            Facebook(post_url, location, prices, max_people, images, rooms,
                     post_time, start_date, end_date, phones))
    return sublets


# TODO [ES] : change dates to latest
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
        location = " ".join([find_airbnb_listing_location(listing["longitude"], listing["latitude"]) + ',', area])
        description = listing['description']
        rating = listing['rating_value']
        reviews = listing['reviews']
        images = listing['photos']
        amenities = listing['amenities']
        max_people = listing['person_capacity']
        prices = listing['price_rate']
        rooms = listing["bedrooms"]  # if listing["bedrooms"] != 0 else None,
        bathrooms = listing["bathrooms"]  # if listing["bathrooms"] != 0 else None,
        beds = listing["beds"]  # if listing["beds"] != 0 else None,
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


def parse_data_from_whatsapp(data):
    group_to_location = {'סאבלט בדפנה': 'דפנה'}
    parser = FreeTextParser()
    sublets = []
    for group_name, messages_per_date in data.items():
        for date1, messages in messages_per_date.items():
            for message in messages:
                if searching_for_sublet('', message['text']):
                    continue
                post_time = datetime.datetime.strptime(date1 + '/' + message['time'], '%m/%d/%Y/%I:%M %p').date()
                start_date, end_date, rooms, _, prices, location, max_people = parser.parse_free_text_to_md(
                    post_text=message['text'], post_time=post_time, listing_location=group_to_location[group_name])
                phone = message['sender']
                # TODO [YG] : parse images by phone number
                sublets.append(WhatsApp(location, prices, max_people, None, rooms, phone, start_date, end_date))


def whatsapp():
    groups = ['סאבלט בדפנה']
    data = download_data_from_groups(groups)
    parse_data_from_whatsapp(data)


def main():
    # airbnb_scraper()
    # airbnb_listings = airbnb_read_data_from_json()
    # sublets = []
    # ws['A1'] = a[2]['text']
    # posts_dict = read_excel_end_create_dict_of_tagged_data(name="facebook_posts_1")
    y = 5
    # excel_data_df = pd.read_excel('/Users/eliyasegev/Desktop/Tagged_data.xlsx', sheet_name='Facebook_data')
    # for column in excel_data_df.columns.ravel():
    # print(column, ": " + str(excel_data_df[column].tolist()))

    # sublets.extend(facebook())
    pass


if __name__ == "__main__":
    main()
