import datetime

from DbHandler import DbHandler


class FacebookSql:

    def __init__(self):
        self.db_handler = DbHandler()

    def dump_to_facebook_raw(self, fb_sublets):
        FaceGroupsRaw_columns = """
                      insert_date,
                      location_city,
                      price_per_night,
                      discounted_price_per_night,
                      discounted_period,
                      minimum_period,
                      max_people,
                      images,
                      rooms_number,
                      rooms_shared,
                      
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
            flat_sublet = (  # Shared data
                datetime.datetime.now(),
                sublet.location.city,
                None,  # price_per_night int     # TODO [AA+YG] : handle price
                None,  # discounted_price_per_night int  # TODO [AA+YG] : handle price
                None,  # discounted_period int   # TODO [AA+YG] : handle price
                None,  # minimum_period int  # TODO [AA+YG] : handle price
                sublet.max_people,
                ','.join(sublet.images),
                sublet.rooms.number,
                sublet.rooms.shared,

                # Facebook data
                sublet.location.street,
                sublet.post_url,
                sublet.post_time,
                sublet.start_date,
                sublet.end_date,
                ','.join(sublet.phones)
            )
            flat_fb_sublets.append(flat_sublet)

        # insert Facebook data into FaceGroupsRaw
        sql = DbHandler.insert_into_string('FaceGroupsRaw', FaceGroupsRaw_columns)
        self.db_handler.cursor.executemany(sql, flat_fb_sublets)
        self.db_handler.connection.commit()
        self.db_handler.close_all()
