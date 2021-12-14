from facebook_scraper import get_posts
from requests_html import HTMLSession
from facebook_scraper import set_proxy, set_user_agent, get_user_agent, get_proxy, reset_proxy, reset_user_agent, get_header
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import pickle
import datetime
from tqdm import tqdm
from Sublet import Sublet
import time
from FacebookGroup import FacebookGroups
import random
import os
import requests

from ParsingFunctions import *
import requests_html
from lxml.html import fromstring
from itertools import cycle


def get_random_proxy():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:1000]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return random.choice(list(proxies))

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
    # credentials = [('avishaya67@gmail.com', '0528773202'), ('yishayahug@mail.tau.ac.il', 'w,+L<e8VjmJ+,6Y')]
    #for fb_group in fb_groups_list_private:
     #   if fb_group not in already_done:
    #        group_posts = []
   #         for post in get_posts(group=fb_group, pages=random.randint(2, 6), # credentials=random.choice(credentials),
  #                                options={"progress": True, "posts_per_page": random.randint(50,
 #                                                                                             100)}):  # TODO : change number of pages and posts per page + add comments?
#                group_posts.append(post)
#            yield fb_group, group_posts
#            time.sleep(random.randint(0, 200))
    for fb_group in fb_groups_list_public:
        if fb_group not in already_done:
            # reset_proxy(get_random_proxy())
            # reset_user_agent(get_useragent())
            print(fb_group)
            print(get_header())
            # print(get_proxy())
            # print(get_user_agent())
            print()
            group_posts = []
            for post in get_posts(group=fb_group, pages=random.randint(1, 2), #credentials=random.choice(credentials),
                                  options={"progress": True, "posts_per_page": random.randint(50, 100)}):  # TODO : change number of pages and posts per page + add comments?
                group_posts.append(post)
            yield fb_group, group_posts
           # time.sleep(random.randint(0, 200))


def parse_data_from_facebook(dict_of_sublets):
    list_of_sublets = []
    for group_id, posts in dict_of_sublets.items():
        for post in posts:
            list_of_sublets.append((group_id, post))
    sublets = []
    for group_id, sublet in tqdm(list_of_sublets):
        post_title = sublet.get('title', '')
        post_text = sublet.get('text')
        if searching_for_sublet(post_title, post_text):
            continue

        assert post_text is not None
        post_url = sublet['post_url']
        post_time = sublet['time']
        start_date, end_date = extract_dates_from_text(post_text)
        location = sublet['listing_location'] if 'listing_location' in sublet else parse_location(post_title,
                                                                                                  post_text,
                                                                                                  group_id)  # TODO : 1.if None-parse from text, if number-figure out what is this number and decide
        rooms = 0  # TODO : parse rooms from text
        prices = {'price_0': sublet['listing_price']} if 'listing_price' in sublet else parse_price(post_title,
                                                                                                    post_text)
        max_people = 0  # TODO : parse max_people from text
        phones = parse_phone_number(post_title, post_text)  # TODO : parse phone from text
        images = sublet['images']
        sublets.append(
            Sublet(post_url, post_time, start_date, end_date, location, rooms, prices, max_people, phones, images))
    return sublets


def facebook():
    dict_of_sublets = pickle.load(open("dict_of_sublets.p", 'rb')) if os.path.exists("dict_of_sublets.p") else {}
    for group_id, group_posts in tqdm(get_data_from_facebook(already_done=set(dict_of_sublets.keys())),
                                       desc='extracting groups data'):
         dict_of_sublets[group_id] = group_posts
         pickle.dump(dict_of_sublets, open('dict_of_sublets.p', 'wb'))
    return parse_data_from_facebook(dict_of_sublets)


def main():
    sublets = []
    sublets.extend(facebook())
    pass


if __name__ == "__main__":
    main()

