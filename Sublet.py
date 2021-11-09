
class Sublet:
    def __init__(self, post_url, post_time,  start_date, end_date, location, rooms, price, max_people, phone, images):
        self.post_url = post_url
        self.post_time = post_time
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.rooms = rooms
        self.price = price
        self.max_people = max_people
        self.phone = phone
        self.images = images # TODO : use images_description from facebook