import time
import mysql.connector
from credential import DB_DATA
from apikey import Apikey


class DatabaseInteractions(object):
    # Create table:
    # mycursor.execute("CREATE TABLE clients (id INT(255), uuid VARCHAR(255), client_name VARCHAR(255), asociated_uuid INT(255))")
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=DB_DATA['host'],
            user=DB_DATA['user'],
            password=DB_DATA['password'],
            database=DB_DATA['database']
        )
        self.mycursor = self.mydb.cursor()

    def add_client(self, name):
        sql = "INSERT rarced.clients (id, client_name, uuid, asociated_uuid) VALUES (%s,%s,%s,%s)"
        # generate the random api key to the new client
        val = (6, name, Apikey().generate_key(32), 0)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def delete_client(self, client):
        sql = "DELETE from rarced.clients where client_name=\"" + \
            str(client)+"\""
        self.mycursor.execute(sql)
        self.mydb.commit()


# sql = DatabaseInteractions()
# sql.add_client("paquito")
# sql.delete_client("paquito")
# For showing all the databases asociated:
# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#     print(x)
