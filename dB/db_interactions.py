import sqlite3
# for connected: .\sqlite3 dbchild
from client_data_priv import clients_info, associated_uuids


class Db_handler (object):

    def __init__(self, path_file):
        self.path_file = path_file
        self.con = None
        if (self.create_connection()):
            print("Connected to db")
        else:
            print("Not able to connect")

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
            #group - texture - FC - WP - EP
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
            #group - A - B - C
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
        #id - client_name - uuid - associated_uuid
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
                client_id INTEGER,
                FOREIGN KEY (client_id)
                    REFERENCES clients (id) 
                );'''
        cur = self.conn.cursor()
        cur.execute(sql_text)
        self.conn.commit()
        #id - client_name - uuid - associated_uuid
        for u in associated_uuids:
            sql_text = '''INSERT INTO uuid_associations(controller_uuid, client_id) VALUES (?,?); '''
            cur = self.conn.cursor()
            cur.execute(sql_text, u)
            self.conn.commit()


db_path = "db_production"
db = Db_handler(db_path)
db._delete_all()
db._create_clients()
db._create_uuid_associations()
# db.create_texture()
# project = (3, "5ºD", "contraseña3", "image", "icon")
# db.add_class(project)
