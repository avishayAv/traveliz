# traveliz

Tasks :
https://docs.google.com/spreadsheets/d/1NTCS35fS4vo4Xg0lFv2fbQUXuI49QivlUAkAYzGnhHw/edit?usp=sharing

Flows :

Facebook scraper : main.py -s facebook -m scrape
Facebook parser :
* main.py -s facebook -m parse -data <pickle_path> 
* main.py -s facebook -m parse (default mock pickle for debug) 

AirBnb
AirBnb scraper : main.py -s airbnb -m scrape (will use the default list of locations to scrape).

AirBnb parser : main.py -s airbnb -m parse -data <name of scraped location e.g "eilat">
