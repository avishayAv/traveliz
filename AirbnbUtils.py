import json
import numpy as np

# git clone and follow follow the instruction at:
# https://github.com/digital-engineering/airbnb-scraper

# my AIRBNB_API_KEY = 'd306zoyjsyarp7ifhu67rjxn52tv0t20'

activate_venv_command = ". ~/env/bin/activate"
airbnb_scraper_dir_path = " ~/airbnb-scraper"
airbnb_data_path = "airbnb_data/"

list_of_locations =[
["jerusalem , IL", "jlm"],
["Tel Aviv , IL", "tlv"],
["Haifa , IL", "haifa"],
["Eilat , IL", "eilat"],
["North, IL", "north"],
["Netanya, IL","netanya"]
]

def find_airbnb_listing_location(long, latt):
    cities = json.load(open("israel_cities.json","rb"))
    a = np.array((long, latt))
    dists = [np.linalg.norm(a - np.array((city['long'], city['latt']))) for city in cities]
    min_index = dists.index(min(dists))
    return cities[min_index]["english_name"]
