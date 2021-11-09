from facebook_scraper import get_posts
import pickle
import datetime
from Sublet import Sublet
import time
from FacebookGroup import FacebookGroups


def get_data_from_facebook():
    fb_groups = FacebookGroups().groups
    fb_groups_list_private = [group.group_id for group in fb_groups if not group.is_public]
    fb_groups_list_public = [group.group_id for group in fb_groups if group.is_public]
    credentials = ('avishaya67@gmail.com', '0528773202')
    list_of_sublets = []
    for fb_group in fb_groups_list_private:
        for post in get_posts(group=fb_group, pages=5, credentials=credentials, options={"progress": True, "posts_per_page": 100}): # TODO : change number of pages and posts per page + add comments?
            list_of_sublets.append(post)
        time.sleep(120)
    for fb_group in fb_groups_list_public:
        for post in get_posts(group=fb_group, pages=5, options={"progress": True, "posts_per_page": 100}): # TODO : change number of pages and posts per page + add comments?
            list_of_sublets.append(post)
        time.sleep(120)
    return list_of_sublets


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
    list_of_sublets = get_data_from_facebook()
    pickle.dump(list_of_sublets, open('list_of_sublets.p', 'wb'))
    # list_of_sublets = pickle.load(open("list_of_sublets.p", 'rb')) # Dummy for time saving
    return parse_data_from_facebook(list_of_sublets)


def main():
    sublets = []
    sublets.extend(facebook())
    pass

if __name__ == "__main__":
    main()