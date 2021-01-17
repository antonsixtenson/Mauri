import sqlite3

class AppSuper():

    def __init__(self):
        self.db = sqlite3.connect("social_tests.db")
        self.c = self.db.cursor()


    # Initialize supervisor (admin) table
    def init_supervisors_table(self):
        self.c.execute('''
               CREATE TABLE IF NOT EXISTS supervisors(
                   id INTEGER NOT NULL PRIMARY KEY,
                   name TEXT,
                   surname TEXT,
                   email TEXT,
                   reg_date INTEGER,
                   group_key INTEGER,
                   access_key INTEGER,
                   password TEXT,
                   FOREIGN KEY (group_key) REFERENCES institutions(id)
               )
           ''')
        self.db.commit()

    # Initializes table for requests made by Supervisors
    def init_super_requests_table(self):
        self.c.execute('''
                CREATE TABLE IF NOT EXISTS super_requests(
                    id INTEGER NOT NULL PRIMARY KEY,
                    super_id INTEGER,
                    user_id INTEGER,
                    request INTEGER,
                    group_key INTEGER,
                    FOREIGN KEY (super_id) REFERENCES supervisors(id),
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (group_key) REFERENCES institutions(id) 
                )  
            ''')
        self.db.commit()


    # Adds supervisor, access_key = 1
    def add_supervisor(self, name, surname, email, reg_date, group_key, password):
        self.c.execute('''INSERT INTO supervisors(name, surname, email, reg_date, group_key, access_key, password)
                            VALUES(?, ?, ?, ?, ?, ?, ?)''', (name.lower(), surname.lower(), email.lower(),
                                                             reg_date, group_key, 1, password))

        self.db.commit()

    # user_id in [0][0] and the request in [1][0]
    def fetch_super_requests(self, user_id):
        self.c.execute('''SELECT id, request FROM super_requests WHERE user_id=?''', (user_id,))
        all_requests = self.c.fetchall()
        return all_requests

    # Push request to user: 0 = IDS-100, 1 - SatisfactionScale
    def push_super_request(self, super_id, user_id, group_key, request):
        self.c.execute('''INSERT INTO super_requests(super_id, user_id, group_key, request) VALUES(?, ?, ?, ?)''', (super_id, user_id, group_key, request))
        self.db.commit()

    # Delete request by its ID
    def drop_super_request(self, req_id):
        self.c.execute('''DELETE FROM super_requests WHERE id=?''', (req_id,))
        self.db.commit()

    # Get supervisor group key by its ID.
    def fetch_super_group_key_by_id(self, super_id):
        self.c.execute('''SELECT group_key FROM supervisors WHERE id=?''', (super_id,))
        return self.c.fetchone()[0]

    def fetch_super_email_pwd(self, email):
        self.c.execute('''SELECT email, password FROM supervisors WHERE email=?''', (email,))
        try:
            user = self.c.fetchone()
            return user
        except:
            return None

    def check_super_email_availability(self, email):
        if (self.fetch_super_email_pwd(email) == None):
            return True
        else:
            return False

    def fetch_super_id_by_email(self, email):
        self.c.execute('''SELECT id FROM supervisors WHERE email=?''', (email,))
        try:
            super_id = self.c.fetchone()[0]
            return super_id
        except:
            return None

    # Insert test supervisors
    def push_test_supervisors(self):
        # REQ-input: name, surname, email, reg_date, group_key, password
        names = ["Janne", "Metthe", "Lena"]
        surname = ["Svensson", "Holmström", "Persson"]
        mail_ending = "@jonkoping.se"
        reg_date = [20210101, 20210102, 20210111]
        for i in range(len(names)):
            self.add_supervisor(names[i], surname[i], names[i] + mail_ending, reg_date[i], i+1, names[i].lower())

