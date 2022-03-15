import pymysql
import datetime


class DbHandler(object):
    # Config
    HOST_NAME = "az1-ss100.a2hosting.com"
    USER_NAME = "traveliz_sharvit"
    PASSWORD = "Rugh1234!"
    PORT = 3306
    DB_NAME = "traveliz_main"

    def __init__(self):
        self.connection = pymysql.connect(
                            host=self.HOST_NAME,
                            user=self.USER_NAME,
                            password=self.PASSWORD,
                            database=self.DB_NAME
                                         )
        self.cursor = self.connection.cursor()

    @staticmethod
    def insert_into_string(table_name, columns):
        values = '%s,' * columns.count(',') + '%s'
        sql = f"""
          INSERT INTO {table_name} ({columns}) 
          VALUES ({values})
          """
        return sql

    def close_all(self):
        self.cursor.close()
        self.connection.close()

    def truncate_table(self, table):
        self.cursor.execute("truncate table %s" % table)

    def add_column(self, table, column_name, column_type):
        self.cursor.execute("ALTER TABLE %s ADD %s %s" % (table, column_name, column_type))

    def drop_column(self, table, column_name):
        self.cursor.execute("ALTER TABLE %s DROP COLUMN %s" % (table, column_name))

    def print_describe_table(self, table):
        self.cursor.execute("SHOW columns FROM %s" % (table))
        description = self.cursor.fetchall()
        field_names = [i[0] for i in self.cursor.description]
        print(field_names)
        for value in description:
            print(value)

base_raw_columns = """
                      creation_date,
                      location_city,
                      price_per_night,
                      discounted_price_per_night,
                      discounted_period,
                      minimum_period,
                      price_per_month,
                      price_per_weekend,
                      max_people,
                      images,
                      rooms_number,
                      rooms_shared,
                """