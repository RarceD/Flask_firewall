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
        self.mycursor.execute("SELECT * FROM rarced.clients;")
        self.number_rows = 0
        for _ in self.mycursor:
            number_rows+=1
        print(number_rows)


    def add_client(self, name):
        sql = "INSERT rarced.clients (client_name, uuid, asociated_uuid) VALUES (%s,%s,%s)"
        # generate the random api key to the new client
        val = (name, Apikey().generate_key(32), 0)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def delete_client(self, client):
        sql = "DELETE from rarced.clients where client_name=\"" + \
            str(client)+"\""
        self.mycursor.execute(sql)
        self.mydb.commit()

    def add_uuid_to_client(self, uuid, client):
        sql = "UPDATE rarced.clients SET client_name=\""+str(uuid)+"\" WHERE uuid=\="+str(uuid)+"\""
        self.mycursor.execute(sql)
        self.mydb.commit()


sql = DatabaseInteractions()
# sql.add_client("paquito")
# sql.delete_client("paquito")
# sql.add_uuid_to_client(client="paquito", uuid="uuid-inventado")

# For showing all the databases asociated:
