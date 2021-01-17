import sqlite3



class AppUsers:

    def __init__(self):
        self.db = sqlite3.connect("social_tests.db")
        self.c = self.db.cursor()

    # Create users table in database social_tests, assign specific ID
    def init_users_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER NOT NULL PRIMARY KEY,
                name TEXT,
                surname TEXT,
                email TEXT,
                age INTEGER,
                sex INTEGER,
                reg_date INTEGER,
                ids100_done INTEGER,
                ids100_date_done INTEGER,
                satisfaction_done INTEGER,
                satisfaction_date_done INTEGER,
                group_key INTEGER,
                points INTEGER,
                access_key INTEGER,
                password TEXT,
                FOREIGN KEY (group_key) REFERENCES institutions(id)
            )
        ''')
        self.db.commit()


    def init_user_requests_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS user_requests(
                id INTEGER NOT NULL PRIMARY KEY,
                user_id INTEGER,
                group_key INTEGER,
                request INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (group_key) REFERENCES institutions(id) 
            )  
        ''')
        self.db.commit()

    # Add user to table users in social_test.db, group_key = 0
    def add_user(self, name, surname, email, age, sex, reg_date, group_key, password):

        # ids100_done is initialized as 0 (not done)
        self.c.execute('''
                INSERT INTO users(name, surname, email, age, sex, reg_date, ids100_done, ids100_date_done,
                satisfaction_done, satisfaction_date_done, group_key, points, access_key, password)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (name.lower(), surname.lower(), email.lower(), age, sex, reg_date,
                        0, -1, 0, -1, group_key, 10, -1, password))
        self.db.commit()

    # Fetches individual users points by id
    def fetch_user_points_by_id(self, user_id):
        self.c.execute('''SELECT points FROM users WHERE id=?''', (user_id,))
        try:
            user_points = self.c.fetchone()
            return user_points[0]
        except:
            return None

    # Push new points value to specific user by user-id
    def push_user_points_by_id(self, points_to_add, user_id):
        new_points_sum = self.fetch_user_points_by_id(user_id) + points_to_add
        print(new_points_sum)
        self.c.execute('''UPDATE users SET points=? WHERE id=?''', (new_points_sum, user_id))
        self.db.commit()

    def push_user_reg_request(self, user_id, group_key):
        self.c.execute('''INSERT INTO user_requests(user_id, group_key, request) VALUES(?, ?, ?)''', (user_id, group_key, 0))
        self.db.commit()

    def fetch_user_reg_requests(self, group_key):
        self.c.execute('''SELECT user_id FROM user_requests WHERE group_key=?''', (group_key,))
        all_requests = self.c.fetchall()
        return all_requests

    def push_user_acc_value_zero(self, user_id):
        self.c.execute('''UPDATE users SET access_key=? WHERE id=?''', (0, user_id))
        self.db.commit()

    def drop_user_reg_request(self, user_id):
        self.c.execute('''DELETE FROM user_requests WHERE user_id=?''', (user_id,))
        self.db.commit()

    def fetch_user_acc_value(self, user_id):
        self.c.execute('''SELECT access_key FROM users WHERE id=?''', (user_id,))
        return self.c.fetchone()[0]

    def fetch_user_id_by_group_key(self, group_key):
        self.c.execute('''SELECT id FROM users WHERE group_key=?''', (group_key,))
        return self.c.fetchall()

    # Search and returns (if found) specific
    # users email and password
    # in table users, searches by email
    # and returns as tuple with 2 values
    # where user[0] - email and user[1] - password
    # return None if nothing is found
    def fetch_user_email_pwd(self, email):
        self.c.execute('''SELECT email, password FROM users WHERE email=?''', (email,))
        try:
            user = self.c.fetchone()
            return user
        except:
            return None

    # Fetch all user credentials from email, returns as tuple
    # where user[0] - email and user[1] - age and user[2] - sex
    # return None if nothing found
    def fetch_user_info_by_id(self, user_id):
        self.c.execute('''SELECT name, surname, email, age, sex, reg_date FROM users WHERE id=?''', (user_id,))
        try:
            user = self.c.fetchone()
            return user
        except:
            return None

    def fetch_user_id_by_email(self, email):
        self.c.execute('''SELECT id FROM users WHERE email=?''', (email,))
        try:
            user_id = self.c.fetchone()
            return user_id
        except:
            return None

    def fetch_user_id_by_email(self, email):
        self.c.execute('''SELECT id FROM users WHERE email=?''', (email,))
        try:
            user_id = self.c.fetchone()
            return user_id[0]
        except:
            return None

    # Deletes single user in table users
    def drop_user(self, user_id):
        self.c.execute('''DELETE FROM users WHERE id=?''', (user_id,))
        self.db.commit()

    # Deletes all entries in table users
    def drop_all_users(self):
        self.c.execute('''DELETE FROM users''')
        self.db.commit()

        return "All users were deleted"

    # Fetch all entries in table users
    def fetch_all(self):
        return self.c.fetchall()

    # Check if email is already registered. If so returns True
    def check_email_availability(self, email):
        if (self.fetch_user_email_pwd(email) == None):
            return True
        else:
            return False

    def push_test_users(self):
        # REQ-input: name, surname, email, age, sex, reg_date, password
        names = ['Anton', 'Malin', 'Daniel', 'Rickard', 'Kim', 'Ronja', 'Lisa']
        surnames = ['Sixtenson', 'Andersson', 'Danielsson', 'Hjärt', 'Silfverstierna', 'Svensson', 'Berg']
        reg_dates = [20210101, 20201001, 20201111, 20200913, 20191001, 20210103, 20201212]
        gmail = '@gmail.com'
        age = [29, 32, 19, 18, 22, 48, 39]
        sex = [0, 1, 0, 0, 2, 1, 1]
        for i in range(len(names)):
            self.add_user(names[i], surnames[i], names[i] + gmail, age[i], sex[i], reg_dates[i], 1, names[i].lower())

