import sqlite3

class AppInst():

    def __init__(self):
        self.db = sqlite3.connect("social_tests.db")
        self.c = self.db.cursor()

    # Initialize institutions table
    def init_institution_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS institutions(
            id INTEGER NOT NULL PRIMARY KEY,
            name TEXT,
            type TEXT
            )
        ''')
        self.db.commit()

    def add_institution(self, name, type):
        self.c.execute('''INSERT INTO institutions(name, type) VALUES(?, ?)''', (name.lower(), type.lower()))
        self.db.commit()


    def fetch_all_institutions(self):
        self.c.execute('''SELECT id, name, type FROM institutions''')
        all = self.c.fetchall()
        return all

    def push_test_institutions(self):
        self.add_institution("Bruksborg", "HVB")
        self.add_institution("Hornö", "SiS")
        self.add_institution("Iris Utvecklingcenter  - Mullsjö", "HVB")
        self.add_institution("Granbacken", "HVB")









