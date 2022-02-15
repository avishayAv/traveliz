import json
import time
import random
import requests
import os
import numpy as np
from Sublet import Airbnb

# in order to use airbnb scraper - git clone and follow the instruction at:
# https://github.com/digital-engineering/airbnb-scraper


AIRBNB_API_KEY = 'd306zoyjsyarp7ifhu67rjxn52tv0t20'
activate_venv_command = ". ~/env/bin/activate"
airbnb_scraper_dir_path = " ~/airbnb-scraper"
list_of_locations = [
    ["jerusalem , IL", "jlm"],
    ["Tel Aviv , IL", "tlv"],
    ["Haifa , IL", "haifa"],
    ["Eilat , IL", "eilat"],
    ["North, IL", "north"],
    ["Netanya, IL", "netanya"]
]

class AirbnbScraper():
    def __init__(self):
        self.scraping_page_limit = 5
        self.min_price_night_dollars = 50
        self.max_price_night_dollars = 300

    def airbnb_scraper(self):
        for location in list_of_locations:
            assert len(location) == 2, f"location field is {location}, should be [<city, country>, <name of json file>]"
            self.get_data_from_airbnb(location=location)
            time.sleep(random.randint(120, 200))

    def get_data_from_airbnb(self,
                             location: list):
        command = f'scrapy crawl airbnb -a query="{location[0]}" -a max_price={str(self.max_price_night_dollars)} -a ' \
                  f'min+price={str(self.min_price_night_dollars)} -o {location[1]}.json' \
                  f' -s CLOSESPIDER_PAGECOUNT={str(self.scraping_page_limit)} '

        os.system('( ' + activate_venv_command + ' && cd ' + airbnb_scraper_dir_path + ' && `' + command + '`)')

#TODO (ES) use location objecy instead of string

class AirbnbParser():
    def __init__(self):
        pass

    def airbnb_read_data_from_json(self):
        listings = []
        for location in list_of_locations:
            airbnb_data = self.parse_airbnb_data(location[1] + ".json")
            listings.extend(airbnb_data)
        return listings

    def parse_airbnb_data(self, json_file_path: str):
        airbnb_data = json.load(open(json_file_path, "rb"))
        airbnb_listings = []
        for listing in airbnb_data:
            name = listing['name']
            post_url = listing['url']
            area = json_file_path.split('/')[-1].split(".")[0]
            location = " ".join([self.find_airbnb_listing_location(listing["longitude"], listing["latitude"]) + ',', area])
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

    @staticmethod
    def get_calendar_of_airbnb_listing_id(listing_id: str,
                                          month: str,
                                          year:str):
        link = f"https://www.airbnb.com/api/v2/calendar_months?key={AIRBNB_API_KEY}" \
               f"&currency=ILS&locale=en&listing_id={listing_id}&month={month}&year={year}&count=1&_format=with_conditions"
        f = requests.get(link)
        myfile = f.text
        try:
            data = json.loads(myfile)
            days = data['calendar_months'][0]['days']
            calander = [{'date': day['date'],
                   'available': day['available'],
                   'min_nigths':day['min_nights'],
                   'price': day['price']['local_price'],
                   'currency': day['price']['local_currency']} for day in days]
            return calander
        except:
            return []

    @staticmethod
    def find_airbnb_listing_location( long, latt):
        cities = json.load(open("israel_cities.json", "rb"))
        a = np.array((long, latt))
        dists = [np.linalg.norm(a - np.array((city['long'], city['latt']))) for city in cities]
        min_index = dists.index(min(dists))
        return cities[min_index]["english_name"]





