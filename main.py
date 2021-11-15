import os
from facebook_scraper import get_posts
import pickle
import datetime
from tqdm import tqdm
from Sublet import Sublet
import time
from FacebookGroup import FacebookGroups
import random


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


def parse_data_from_facebook(list_of_sublets):
    sublets = []
    for sublet in list_of_sublets:
        post_url = sublet['post_url']
        post_time = sublet['time']
        start_date = ''  # TODO : parse start_date from text
        end_date = ''  # TODO : parse end_date from text
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
