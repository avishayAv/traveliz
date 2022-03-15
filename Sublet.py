import datetime
from dataclasses import dataclass
from typing import Union, Optional

from PriceParser import Price


class Rooms:
    def __init__(self):
        self.number = None
        self.shared = False


@dataclass
class Location:
    city: str
    street: str


class Sublet:
    def __init__(self, location: Location, price: Price,
                 max_people: int, images: [str], rooms: Optional[Union[int, float]]):
        self.location = location
        self.prices = price
        self.max_people = max_people
        self.images = images  # TODO : use images_description from facebook
        self.rooms = rooms


class Facebook(Sublet):
    def __init__(self, post_url, location, prices, max_people, images, rooms,
                 post_time: datetime, start_date: datetime, end_date: datetime, phones: set):
        super().__init__(location, prices, max_people, images, rooms)
        self.post_url = post_url
        self.post_time = post_time
        self.start_date = start_date
        self.end_date = end_date
        self.phones = phones



class Airbnb(Sublet):
    def __init__(self, post_url, location, price, max_people, images, rooms,
                 name: str, description: str, rating: Optional[int], reviews: Optional[list],
                 amenities: list, bathrooms: Optional[Union[int, float]], beds: Optional[int]):
        super().__init__(location, price, max_people, images, rooms)
        self.post_url = post_url
        self.name = name
        self.description = description
        self.rating = rating
        self.reviews = reviews
        self.amenities = amenities
        self.bathrooms = bathrooms
        self.beds = beds

    # TODO [ES] : after creating DB - create function that add calendar to existing listing
    # def add_calendar_to_listing(self, calendar: list):
    #     self.calendar = calendar


class WhatsApp(Sublet):
    def __init__(self, location, prices, max_people, images, rooms, post_time, phone, start_date, end_date,
                 post_text, group_name):
        super().__init__(location, prices, max_people, images, rooms)
        self.post_time = post_time
        self.phone = phone
        self.start_date = start_date
        self.end_date = end_date
        self.post_text = post_text
        self.group_name = group_name
