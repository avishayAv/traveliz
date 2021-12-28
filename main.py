import os
import pickle
import random
import time

from facebook_scraper import get_posts
from facebook_scraper import set_user_agent
from facebook_scraper import FacebookScraper
from tqdm import tqdm

from ParsingFunctions import *
from Sublet import Facebook, WhatsApp
from utils import whatsapp_group_to_location
#from whatsapp_utils import download_data_from_groups

import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def get_useragent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    # Get list of user agents.
    useragents = user_agent_rotator.get_user_agents()
    useragentTemp = random.choice(list(useragents))
    useragent = useragentTemp.get('user_agent')
    return useragent


def get_data_from_facebook(already_done):
    fb_groups = FacebookGroups().groups
    fb_groups_list_private = [group.group_id for group in fb_groups if not group.is_public]
    fb_groups_list_public = [group.group_id for group in fb_groups if group.is_public]
    # credentials = [('yishayahug@mail.tau.ac.il', 'Password1!')]
    # for fb_group in fb_groups_list_private:
    #     if fb_group not in already_done:
    #         group_posts = []
    #         for post in get_posts(group=fb_group, pages=random.randint(2, 6), credentials=random.choice(credentials),
    #                               options={"progress": True, "posts_per_page": random.randint(50,
    #                                                                                           100)}):  # TODO : change number of pages and posts per page + add comments?
    #             group_posts.append(post)
    #         yield fb_group, group_posts
    #         time.sleep(random.randint(0, 200))
    for fb_group in fb_groups_list_public:
        if fb_group not in already_done:
            group_posts = []
            for post in get_posts(group=fb_group, pages=random.randint(5, 10), # credentials=random.choice(credentials),
                                  options={"progress": True, "posts_per_page": random.randint(50, 100)}):  # TODO : change number of pages and posts per page + add comments?
                group_posts.append(post)
            yield fb_group, group_posts
            random_sleep = random.randint(100, 300)
            print(f"Going to sleep for {random_sleep} seconds")
            time.sleep(random.randint(100, 300))
            _scraper = FacebookScraper()


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


def parse_rooms_and_dates_from_facebook(post_text, post_time):
    rooms, masked_text = extract_rooms_from_text(post_text)
    start_date, end_date = extract_dates_from_text(masked_text, post_time)
    return end_date, rooms, start_date


def facebook():
    dict_of_sublets = pickle.load(open("dict_of_sublets_week_trial.p", 'rb')) if os.path.exists("dict_of_sublets_week_trial.p") else {}
    for group_id, group_posts in tqdm(get_data_from_facebook(already_done=set(dict_of_sublets.keys())),
                                      desc='extracting groups data'):
        dict_of_sublets[group_id] = group_posts
        pickle.dump(dict_of_sublets, open('dict_of_sublets_week_trial.p', 'wb'))
    return parse_data_from_facebook(dict_of_sublets)


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
                                            WhatsApp(location, prices, max_people, None, rooms, phone, start_date,
                                                     end_date)])
    return sublets

# def whatsapp():
#     groups = ['סאבלט בדפנה']
#     data = download_data_from_groups(groups)
#     return parse_data_from_whatsapp(data)


def main():
    # parser = AirbnbParser()
    # res = parser.parse_airbnb_data(json_file_path = "airbnb_data/jlm.json")
    # scraper = AirbnbScraper()
    # scraper.airbnb_scraper()
    # airbnb_listings = airbnb_read_data_from_json()
    sublets = []
    # ws['A1'] = a[2]['text']
    # create_excel_for_tagging_data()
    # posts_dict = read_excel_end_create_dict_of_tagged_data(name="facebook_posts_1")
    # if not os.path.exists('sublets_from_whatsapp.p'):
    #     pickle.dump(whatsapp(), open('sublets_from_whatsapp.p', 'wb'))
    # else:
    #     x = pickle.load(open('sublets_from_whatsapp.p', 'rb'))

    # y = 5
    # excel_data_df = pd.read_excel('/Users/eliyasegev/Desktop/Tagged_data.xlsx', sheet_name='Facebook_data')
    # for column in excel_data_df.columns.ravel():
    # print(column, ": " + str(excel_data_df[column].tolist()))

    sublets.extend(facebook())
    # pass


if __name__ == "__main__":
    main()
