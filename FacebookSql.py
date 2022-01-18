import datetime
import pymysql
import DbHandler


class FacebookSql:

    def __init__(self):
        self.connection = DbHandler()
        self.cursor = self.connection.cursor()

    def dump_to_facebook_raw(self, fb_sublets):
        # Flat Facebook Data
        flat_fb_sublets = []
        for sublet in fb_sublets:
            flat_sublet = (  # Shared data
                datetime.datetime.now(),
                sublet.location.city,
                sublet.location.street,
                None,  # price_per_night int     # TODO [AA+YG] : handle price
                None,  # discounted_price_per_night int  # TODO [AA+YG] : handle price
                None,  # discounted_period int   # TODO [AA+YG] : handle price
                None,  # minimum_period int  # TODO [AA+YG] : handle price
                sublet.max_people,
                ','.join(sublet.images),
                sublet.rooms.number,
                sublet.rooms.shared,

                # Facebook data
                sublet.post_url,
                sublet.post_time,
                sublet.start_date,
                sublet.end_date,
                ','.join(sublet.phones)
            )
            flat_fb_sublets.append(flat_sublet)

        # insert Facebok data into FaceGroupsRaw
        self.cursor.executemany("""
                      INSERT INTO FaceGroupsRaw (insert_date,
                      location_city,
                      location_street,
                      price_per_night,
                      discounted_price_per_night,
                      discounted_period,
                      minimum_period,
                      max_people,
                      images,
                      rooms_number,
                      rooms_shared,
                      post_url,
                      post_time,
                      start_date,
                      end_date,
                      phones)
                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", flat_fb_sublets)

        self.connection.commit()
        self.cursor.close()
        self.connection.close()


