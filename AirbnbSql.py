import datetime

from DbHandler import DbHandler
from DbHandler import base_raw_columns


class AirbnbSql:

    def __init__(self):
        self.db_handler = DbHandler()

    def dump_to_airbnb_raw(self, airbnb_sublets):
        AirbnbGroupsRaw_columns = base_raw_columns + """
                                                     post_url,
                                                     rating,
                                                     description,
                                                     start_date,
                                                     end_date
                                                     """
        # Flat Airbnb Data
        flat_airbnb_sublets = []
        for sublet in airbnb_sublets:
            flat_sublet = (
                # Base columns
                datetime.datetime.now(),    # creation_date
                None,                       # location_city
                None,                       # price_per_night int
                None,                       # discounted_price_per_night int
                None,                       # discounted_period int
                None,                       # minimum_period int
                None,                       # price_per_month
                None,                       # price_per_weekend
                sublet.max_people,          # max_people
                None,                       # images
                sublet.rooms,               # rooms_number
                None,                       # rooms_shared
                # Airbnb data
                sublet.post_url,            # post_url
                sublet.rating,              # rating
                sublet.description,         # description
                None,                       # start_date
                None,                       # end_date
                )
            flat_airbnb_sublets.append(flat_sublet)

        # insert airbnb data into AirbnbRaw
        sql = DbHandler.insert_into_string('AirbnbRaw', AirbnbGroupsRaw_columns)
        self.db_handler.cursor.executemany(sql, flat_airbnb_sublets)
        self.db_handler.connection.commit()
        self.db_handler.close_all()