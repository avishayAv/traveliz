import pymysql

class DbHandler:
    # Config
    HOST_NAME = "traveliz2.c7izxvnjnup5.us-east-1.rds.amazonaws.com"
    USER_NAME = "admin"
    PASSWORD = "DontWorry2027"
    PORT = 3306
    DB_NAME = "Traveliz"

    def __init__(self):
        self.connection = pymysql.connect(host=self.HOST_NAME,
                            user=self.USER_NAME,
                             password=self.PASSWORD,
                             database=self.DB_NAME,
                             cursorclass=pymysql.cursors.DictCursor)


    def show_all_rows(self, table):
        query = "select * from {table}"
        result =  mycursor.execute("select * from %s" % table)
        result = (mycursor.fetchall())
        for row in result:
            print(row, '\n')


    def truncate_table(mycursor, table):
        mycursor.execute("truncate table %s" % table)


    def add_column(mycursor, table, column_name, column_type):
        mycursor.execute("ALTER TABLE %s ADD %s %s" % (table, column_name, column_type))


    def drop_column(mycursor, table, column_name):
        mycursor.execute("ALTER TABLE %s DROP COLUMN %s" % (table, column_name))

