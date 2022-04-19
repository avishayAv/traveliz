import datetime
from DbHandler import DbHandler
from DbHandler import base_raw_columns
from utils import whatsapp_groups_to_scrape_and_parse
class WhatsappSql:

    def __init__(self):
        self.db_handler = DbHandler()

    def dump_to_whatsapp_raw(self, wa_sublets):
        WhatsGroupsRaw_columns = base_raw_columns + """
                                                    location_street,
                                                    post_time,
                                                    start_date,
                                                    end_date,
                                                    phones,
                                                    post_text,
                                                    group_name                                              """
        # Flat Whatsapp Data
        flat_wa_sublets = [] #TODO [RS]: delete text+date form whatsapp class (they are already in the whatsapp object)
        for group in whatsapp_groups_to_scrape_and_parse:
            for sublet in wa_sublets[group]:
                flat_sublet = (
                    # Base columns
                    datetime.datetime.now(),    # insert_date
                    sublet.location.city,       # location_city
                    None,                       # price_per_night int     # TODO [AA+YG] : handle price
                    None,                       # discounted_price_per_night int  # TODO [AA+YG] : handle price
                    None,                       # discounted_period int   # TODO [AA+YG] : handle price
                    None,                       # minimum_period int  # TODO [AA+YG] : handle price
                    None,                       # price_per_month # TODO [AA+YG] : handle price
                    None,                       # price_per_weekend # TODO [AA+YG] : handle price
                    sublet.max_people,          # max_people
                    None,                       # images
                    sublet.rooms.number,        # rooms_number
                    sublet.rooms.shared,        # rooms_shared
                    # Facebook data
                    sublet.location.street,     # location_street
                    sublet.post_time,           # post_time
                    sublet.start_date,          # start_date
                    sublet.end_date,            # end_date
                    sublet.phone,               # phone
                    sublet.post_text,           # post_text
                    sublet.group_name           # group_name
                )
                flat_wa_sublets.append(flat_sublet)

            # insert Whatsapp data into WhatsGroupsRaw
            sql = DbHandler.insert_into_string('WhatsGroupsRaw', WhatsGroupsRaw_columns)
            self.db_handler.cursor.executemany(sql, flat_wa_sublets)
            self.db_handler.connection.commit()
            self.db_handler.close_all()