import time
import mysql.connector
from credential import DB_DATA
from apikey import Apikey
from dB.db_interactions import Db_handler
from dB.client_data_priv import SQL_COMMANDS, AVAILABLE_CROPS

"""
Get data from other database in order to ger sensor data:
"""


class DatabaseInteractions(object):
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=DB_DATA['host'],
            user=DB_DATA['user'],
            password=DB_DATA['password'],
            database=DB_DATA['database']
        )
        self.mycursor = self.mydb.cursor()

    def _get_devices(self):
        self.mycursor.execute(SQL_COMMANDS['devices'])
        self.number_rows = 0
        for m in self.mycursor:
            print(m)

    def _get_node_id_fuck_api(self):
        self.mycursor.execute(SQL_COMMANDS['dataloger'])
        self.number_rows = 0
        for m in self.mycursor:
            print(m)

    def _get_smart_irrigation(self):
        self.mycursor.execute(SQL_COMMANDS['smart_irrigation'])
        self.number_rows = 0
        for m in self.mycursor:
            print(m)

    def _get_nap_parameters_A_B_C(self, crop_name):
        # First I obtein the crop id
        if any(str(crop_name) in s for s in AVAILABLE_CROPS):
            sql_command = '''SELECT * FROM crops WHERE code="''' + crop_name + '''";'''
            self.mycursor.execute(sql_command)
            nap_group = 0
            for m in self.mycursor:
                nap_group = m[7]
            print("NAP group", nap_group)
            # Second get the values of the A, B, C params:
            sql_command = "SELECT NAP_A,NAP_B,NAP_C FROM group_naps WHERE id=" + \
                str(nap_group) + ";"
            self.mycursor.execute(sql_command)
            for m in self.mycursor:
                naps_abc = m
            print("NAP_A, B, C", naps_abc)    
        else:
            print("Not found the crop")

    def __del__(self):
        self.mydb.close()


sql = DatabaseInteractions()
sql._get_nap_parameters_A_B_C("Tabaco")
