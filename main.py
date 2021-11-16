import os.path
import re

from datetime import datetime
import dateutil.parser as dparser

from facebook_scraper import get_posts
import pickle
import datetime
from Sublet import Sublet
import time
from FacebookGroup import FacebookGroups
from DateParser import DatePatterns, DateReg


def get_data_from_facebook():
    fb_groups = FacebookGroups().groups
    fb_groups_list_private = [group.group_id for group in fb_groups if not group.is_public]
    fb_groups_list_public = [group.group_id for group in fb_groups if group.is_public]
    credentials = ('avishaya67@gmail.com', '0528773202')
    list_of_sublets = []
    for fb_group in fb_groups_list_private:
        for post in get_posts(group=fb_group, pages=5, credentials=credentials, options={"progress": True, "posts_per_page": 100}): # TODO : change number of pages and posts per page + add comments?
            list_of_sublets.append(post)
        time.sleep(500)
    for fb_group in fb_groups_list_public:
        for post in get_posts(group=fb_group, pages=5, options={"progress": True, "posts_per_page": 100}): # TODO : change number of pages and posts per page + add comments?
            list_of_sublets.append(post)
        time.sleep(500)
    return list_of_sublets

# do not use datefinder - not working well with hebrew
def extract_dates_from_text(text):
    dates = []
    for date_pattern in DatePatterns().patterns:
        dates_regex = [DateReg(x, date_pattern, "." in x) for x in re.findall(date_pattern.pattern, text)]
        for date_regex in dates_regex:
            date_regex.complete_year()
        dates.extend(dates_regex)
        if (date_pattern.name.startswith('combined') and len(dates) >= 1) or len(dates) >= 2:
            break

    # Prioritize ranged dates
    patterns = [d.date_pattern.is_range for d in dates] # TODO [AA] - 1. handle empty case  2. handle ranged case
    if True in patterns or len(patterns) == 0:
        return 'a', 'b'

    real_dates = [dparser.parse(i.date, fuzzy=True, dayfirst=True).date() for i in dates]
    return min(real_dates), max(real_dates)


def parse_data_from_facebook(dict_of_sublets):
    list_of_sublets = []
    for v in dict_of_sublets.values():
        list_of_sublets.extend(v)
    sublets = []
    for sublet in list_of_sublets:
        post_url = sublet['post_url']
        post_time = sublet['time']
        start_date, end_date = extract_dates_from_text(sublet['text']) # TODO [AA] : should be list (in case of multiple date options)
        location = sublet.get(
            'listing_location')  # TODO : 1.if None-parse from text, if number-figure out what is this number and decide
        rooms = 0  # TODO : parse rooms from text
        price = sublet.get('listing_price')  # TODO : if None-parse from text
        max_people = 0  # TODO : parse max_people from text
        phone = ''  # TODO : parse phone from text
        images = sublet['images']
        sublets.append(
            Sublet(post_url, post_time, start_date, end_date, location, rooms, price, max_people, phone, images))
    return sublets


def facebook():
    if os.path.exists('dict_of_sublets.p'): # Dummy for time saving
        list_of_sublets = pickle.load(open('dict_of_sublets.p','rb'))
    else:
        list_of_sublets = get_data_from_facebook()
        pickle.dump(list_of_sublets, open('dict_of_sublets.p', 'wb'))
    return parse_data_from_facebook(list_of_sublets)


def main():
    sublets = []
    sublets.extend(facebook())
    pass

if __name__ == "__main__":
    main()