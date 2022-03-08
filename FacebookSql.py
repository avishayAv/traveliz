import datetime

from DbHandler import DbHandler
from DbHandler import base_raw_columns



class FacebookSql:

    def __init__(self):
        self.db_handler = DbHandler()

    def dump_to_facebook_raw(self, fb_sublets):
        FaceGroupsRaw_columns = base_raw_columns + """
                                                    location_street,
                                                    post_url,
                                                    post_time,
                                                    start_date,
                                                    end_date,
                                                    phones
                                                    """

        # Flat Facebook Data
        flat_fb_sublets = []
        for sublet in fb_sublets:
            flat_sublet = (
                # Base columns
                datetime.datetime.now(),  # insert_date
                sublet.location.city,  # location_city
                None,  # price_per_night int     # TODO [AA+YG] : handle price
                None,  # discounted_price_per_night int  # TODO [AA+YG] : handle price
                None,  # discounted_period int   # TODO [AA+YG] : handle price
                None,  # minimum_period int  # TODO [AA+YG] : handle price
                None,  # price_per_month TODO [AA+YG] : handle price
                None,  # price_per_weekend TODO [AA+YG] : handle price
                sublet.max_people,  # max_people
                ','.join(sublet.images),  # images
                sublet.rooms.number,  # rooms_number
                sublet.rooms.shared,  # rooms_shared
                sublet.location.street,  # location_street
                sublet.post_url,  # post_url
                sublet.post_time,  # post_time
                sublet.start_date,  # start_date
                sublet.end_date,  # end_date
                ','.join(sublet.phones)  # phones
            )
            flat_fb_sublets.append(flat_sublet)

        # insert Facebook data into FaceGroupsRaw
        sql = DbHandler.insert_into_string('FaceGroupsRaw', FaceGroupsRaw_columns)
        self.db_handler.cursor.executemany(sql, flat_fb_sublets)
        self.db_handler.connection.commit()
        self.db_handler.close_all()
