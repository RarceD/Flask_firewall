import sqlite3
import time
# for connected: .\sqlite3 dbchild
from dB.client_data_priv import clients_info, associated_uuids, uuid_received_test, client_received_test


class Db_handler (object):

    def __init__(self, path_file):
        self.path_file = path_file
        self.con = None
        if (self.create_connection()):
            pass
        # else:
        #     print("Not able to connect")

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.path_file)
            """
            Create the databases:
                self._create_textures()
                self._create_nap()
            """
            return True
        except:
            return False

    def _create_textures(self):
        try:
            sql_text = '''CREATE TABLE textures (
                id integer,
                name_texture text,
                fc text,
                wp text,
                ep text
                );'''
            cur = self.conn.cursor()
            cur.execute(sql_text)
            self.conn.commit()
            # group - texture - FC - WP - EP
            texture_info = [
                (1,  "Arenoso", 0.100	, 0.033	, 0.437),
                (2,  "Arenoso Franco", 0.135	, 0.055	, 0.437),
                (3,  "Franco Arenoso", 0.180	, 0.065	, 0.453),
                (4,  "Franco", 0.240	, 0.095	, 0.463),
                (5,  "Franco Limoso"	, 0.260	, 0.110	, 0.501),
                (6,  "Franco Arcillo Arenoso", 0.270	, 0.115	, 0.498),
                (7,  "Franco Arcilloso", 0.295	, 0.143	, 0.464),
                (8,  "Franco Arcillo Limoso"	, 0.320	, 0.170	, 0.471),
                (9,  "Arcillo Arenoso", 0.325, 0.190	, 0.430),
                (10, "Arcillo Limoso", 0.330, 0.205	, 0.479),
                (11, "Arcilloso", 0.340	, 0.225	, 0.475)
            ]
            for t in texture_info:
                self._add_texture(t)
            return True
        except:
            return False

    def _create_nap(self):
        try:
            sql_text = '''CREATE TABLE nap (
                id integer,
                A real,
                B real,
                C real
                );'''
            cur = self.conn.cursor()
            cur.execute(sql_text)
            self.conn.commit()
            # group - A - B - C
            nap_info = [
                (1, 0.850, 1.585, 0.405),
                (2, 0.786, 3.501, 0.472),
                (3, 0.692, 6.657, 0.542),
                (4, 0.606, 11.860, 0.602)
            ]
            for n in nap_info:
                self._add_nap(n)
            return True
        except:
            return False

    def _add_texture(self, texture_parameters):
        sql_text = ''' INSERT INTO textures(id, name_texture, fc, wp, ep)
                    VALUES (?,?,?,?,?); '''
        cur = self.conn.cursor()
        cur.execute(sql_text, texture_parameters)
        self.conn.commit()

    def _add_nap(self, class_parameters):
        sql_text = ''' INSERT INTO nap (id, A, B, C)
                    VALUES (?,?,?,?); '''
        cur = self.conn.cursor()
        cur.execute(sql_text, class_parameters)
        self.conn.commit()

    def _create_clients(self):
        sql_text = '''CREATE TABLE clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT,
                uuid TEXT,
                associated_uuid INTEGER
                );'''
        cur = self.conn.cursor()
        cur.execute(sql_text)
        self.conn.commit()
        # id - client_name - uuid - associated_uuid
        for c in clients_info:
            sql_text = '''INSERT INTO clients(client_name, uuid, associated_uuid) VALUES (?,?,?); '''
            cur = self.conn.cursor()
            cur.execute(sql_text, c)
            self.conn.commit()

    def _delete_all(self):
        sql_text = '''DROP TABLE clients;'''
        cur = self.conn.cursor()
        cur.execute(sql_text)
        self.conn.commit()
        sql_text = '''DROP TABLE uuid_associations;'''
        cur = self.conn.cursor()
        cur.execute(sql_text)
        self.conn.commit()

    def _create_uuid_associations(self):
        sql_text = '''CREATE TABLE uuid_associations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                controller_uuid TEXT,
                client_id INTEGER NOT NULL,
                FOREIGN KEY (client_id)
                REFERENCES clients (id)
                    ON UPDATE RESTRICT
                    ON DELETE RESTRICT
                );'''
        cur = self.conn.cursor()
        cur.execute(sql_text)
        self.conn.commit()
        # id - client_name - uuid - associated_uuid
        for u in associated_uuids:
            sql_text = '''INSERT INTO uuid_associations(controller_uuid, client_id) VALUES (?,?); '''
            cur = self.conn.cursor()
            cur.execute(sql_text, u)
            self.conn.commit()

    def check_uuid_is_association(self, uuid_received, client_received):
        try:
            # First I get the client id from the uuid_associations table:
            sql_text = """SELECT client_id  FROM uuid_associations WHERE "controller_uuid"=?;"""
            cur = self.conn.cursor()
            cur.execute(sql_text, [(uuid_received)])
            db_client_id_table_uuid_assocaitions = cur.fetchall()[0][0]
            # print("The client_id in controller_uuid table is",
            #     db_client_id_table_uuid_assocaitions)
            # Second I get the id from the clients table:
            sql_text = """SELECT id  FROM clients WHERE "uuid"=?;"""
            cur = self.conn.cursor()
            cur.execute(sql_text, [(client_received)])
            db_client_id_table_clients = cur.fetchall()[0][0]
            # print("The client_id in client table is", db_client_id_table_clients)
            # Third get the name of the client:
            sql_text = """SELECT client_name FROM clients WHERE "uuid"=?;"""
            cur = self.conn.cursor()
            cur.execute(sql_text, [(client_received)])
            client_name_info = cur.fetchall()[0][0]
            # print("The client_name in client table is", client_name_info)
        except:
            return False

        if (db_client_id_table_uuid_assocaitions == db_client_id_table_clients):
            self._add_popularity(client_name_info)
            return True
        else:
            print("Not now")
            return False

    def check_popularity(self, client):
        # Get all the client that has request interactions:
        try:
            sql_text = """CREATE TABLE popularity (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT,
                        time_request TEXT);"""
            cur = self.conn.cursor()
            cur.execute(sql_text)
            self.conn.commit()
            cur.close()
        except:
            pass
        try:
            sql_text = """SELECT COUNT (*) FROM popularity WHERE client_name=?;"""
            cur = self.conn.cursor()
            cur.execute(sql_text, [client])
            cur.close()
            return (cur.fetchall()[0][0])
        except:
            return "this client does not exist"

    def _add_popularity(self, client_received):
        sql_text = '''INSERT INTO popularity(client_name, time_request) VALUES (?,?); '''
        cur = self.conn.cursor()
        cur.execute(sql_text, (client_received, str(time.ctime())))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# db_path = "db_production"
# db = Db_handler(db_path)
# db.create_db()
# db._delete_all()
# db.create_texture()
# db._create_clients()
# db._create_uuid_associations()
# db.check_uuid_is_association(uuid_received=uuid_received_test,
#                              client_received=client_received_test)
# print(db.check_popularity("RARCED"))
