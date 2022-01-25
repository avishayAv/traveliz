import pymysql
import datetime


class DbHandler(object):
    # Config
    HOST_NAME = "traveliz2.c7izxvnjnup5.us-east-1.rds.amazonaws.com"
    USER_NAME = "admin"
    PASSWORD = "DontWorry2027"
    PORT = 3306
    DB_NAME = "Traveliz"

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
