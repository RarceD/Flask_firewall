import time
import mysql.connector
from credential import DB_DATA
from dB.apikey import Apikey
from dB.db_interactions import Db_handler
from dB.client_data_priv import SQL_COMMANDS, AVAILABLE_CROPS, AVAILABLE_TEXTURES

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

    def get_nap_parameters_crop(self, crop_name):
        nap_group = 0
        id_group = 0
        naps_abc = 0
        kcs_list = []
        crop_kc = ""

        # First I obtein the crop id
        if any(str(crop_name) in s for s in AVAILABLE_CROPS):
            sql_command = '''SELECT * FROM crops WHERE code="''' + crop_name + '''";'''
            self.mycursor.execute(sql_command)
            for m in self.mycursor:
                nap_group = m[7]
                id_group = m[0]
            sql_command = "SELECT * FROM crops_provinces WHERE crop_id=" + \
                str(id_group) + ";"
            self.mycursor.execute(sql_command)
            for m in self.mycursor:
                kcs_list = [str(m[5]), str(m[6]), str(m[7]),
                            str(m[8]), str(m[9]), str(m[10])]
                crop_kc = m[1]
            # Second get the values of the A, B, C params:
            sql_command = "SELECT NAP_A,NAP_B,NAP_C FROM group_naps WHERE id=" + \
                str(nap_group) + ";"
            self.mycursor.execute(sql_command)
            for m in self.mycursor:
                naps_abc = m
            returned_parameters = {
                "nap_group": nap_group,
                "id_group": id_group,
                "naps_abc": naps_abc,
                "kcs_list": kcs_list,
                "crop_kc": crop_kc,
            }
            return returned_parameters
        else:
            return "Not found the crop"

    def get_parameters_plot(self, plot_type):
        if any(str(plot_type) in s for s in AVAILABLE_TEXTURES):
            sql_command = '''SELECT FC, WP, EP FROM soils WHERE code="''' + \
                str(plot_type) + '''";'''
            self.mycursor.execute(sql_command)
            self.number_rows = 0
            for m in self.mycursor:
                parameters = {
                    "fc":m[0],
                    "wp":m[1],
                    "ep":m[2]
                }
            return parameters
        else:
            return "Not found the plot"

    def __del__(self):
        self.mydb.close()


