import json
import mysql.connector


def connect_to_db():
    mydb = mysql.connector.connect(
        host='sql6.freesqldatabase.com',
        user='sql6463228',
        password='8iA43qgvtk',
        port='3306',
        database='sql6463228'
    )
    return mydb


def show_all_rows(mycursor, table):
    mycursor.execute("select * from %s" % table)
    result = (mycursor.fetchall())
    for row in result:
        print(row, '\n')


def truncate_table(mycursor, table):
    mycursor.execute("truncate table %s" % table)


def add_column(mycursor, table, column_name, column_type):
    mycursor.execute("ALTER TABLE %s ADD %s %s" % (table, column_name, column_type))


def drop_column(mycursor, table, column_name):
    mycursor.execute("ALTER TABLE %s DROP COLUMN %s" % (table, column_name))


def import_json_into_table_facebook(connection, curser, file_name, table_name):
    json_data = open(file_name).read()
    json_obj = json.loads(json_data)
    for item in json_obj:
        postid = item.get('postid')
        city = item.get('city')
        lastname = item.get('lastname')
        email = item.get('email')
        curser.execute('insert into '+table_name+' (postid, city, lastname, email) value(%s,%s,%s,%s)',
                       (postid, city, lastname, email))
    connection.commit()


def main():
    # open a connection
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    #import Json into table
    import_json_into_table_facebook(mydb, mycursor, 'SQL_test_sharvit', 'Facebook1')
    show_all_rows(mycursor, 'Facebook1')


if __name__ == "__main__":
    main()