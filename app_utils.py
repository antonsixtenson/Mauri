import sqlite3
import ids_100_questions


class AppUtils():

    def __init__(self):
        self.db = sqlite3.connect("social_tests.db")
        self.c = self.db.cursor()

    # Create Table for questions and assign them an specific ID
    def init_ids100_questions_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS ids100_questions(
                id INTEGER NOT NULL PRIMARY KEY,
                question VARCHAR
            )       
        ''')

        q = ids_100_questions.IdsQuestions()
        for i in range(100):
            self.c.execute('INSERT INTO ids100_questions(question) VALUES(?)', (q.return_question(i),))
        self.db.commit()

        # Initializes table for storing answers of every user from the IDS-100 form
    def init_ids100_answer_table(self):
        self.c.execute('''
                CREATE TABLE IF NOT EXISTS ids100_answers(
                    id INTEGER NOT NULL PRIMARY KEY,
                    user_id INTEGER,
                    question_id INTEGER,
                    answer INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (question_id) REFERENCES ids100_questions(id)
                )       
            ''')
        self.db.commit()

    # Initializes table for storing satisfaction scale questions
    def init_satisfaction_scale_questions(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS satisfaction_questions(
                id INTEGER NOT NULL PRIMARY KEY,
                question VARCHAR
            )
        ''')

        q = ["Boende", "Fysisk Hälsa", "Arbete", "Ekonomi", "Alkohol", "Narkotika",
             "Spel", "Juridiska frågor", "Familj, socialt umgänge", "Fritid", "Psykisk Hälsa",
             "Kommunikation ", "Allmänt välbefinnande"]

        for i in range(len(q)):
            self.c.execute('INSERT INTO satisfaction_questions(question) VALUES(?)', (q[i],))
        self.db.commit()

    # Inits table for answers on satisfaction scale questions
    def init_satisfaction_answers(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS satisfaction_answers(
                id INTEGER NOT NULL PRIMARY KEY,
                question_id INTEGER,  
                user_id INTEGER,
                answer_value INTEGER,
                FOREIGN KEY (question_id) REFERENCES satisfaction_questions(id)
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        self.db.commit()

    # Initializes table for storing sums of IDS-100 questions.
    def init_ids100_sums(self):
        self.c.execute('''
             CREATE TABLE IF NOT EXISTS ids100_sums(
                 id INTEGER NOT NULL PRIMARY KEY,
                 sum_0 INTEGER,
                 sum_1 INTEGER,
                 sum_2 INTEGER,
                 sum_3 INTEGER,
                 sum_4 INTEGER,
                 sum_5 INTEGER,
                 sum_6 INTEGER,
                 sum_7 INTEGER,
                 user_id INTEGER,
                 FOREIGN KEY (user_id) REFERENCES users(id)
             )

         ''')
        self.db.commit()

    # Sets ids100_done value in table users to 1
    def push_ids100_test_done(self, user_id):
        self.c.execute('''UPDATE users SET ids100_done=? WHERE id=?''', (1, user_id))
        self.db.commit()

    # Fetch specific users answers to ids100-forms questions. Returns list of tuples as so:
    # [(question_id, value)]
    def fetch_ids100_user_answers(self, user_id):
        self.c.execute('''SELECT question_id, answer FROM ids100_answers
                            INNER JOIN users ON users.id = ids100_answers.user_id WHERE user_id=?''', (user_id,))
        value = self.c.fetchall()
        return value

    # Insert value to specific question, by specific user
    def push_ids100_question_value(self, question_id, user_id, answer):
        self.c.execute('''
            INSERT INTO ids100_answers(question_id, user_id, answer)
            VALUES(?, ?, ?)''', (question_id, user_id, answer))
        self.db.commit()

    # Add calculated sums to it own table
    def push_ids100_sums(self, sum_0, sum_1, sum_2, sum_3, sum_4, sum_5, sum_6, sum_7, user_id):
        self.c.execute('''
            INSERT INTO ids100_sums(sum_0, sum_1, sum_2, sum_3, sum_4, sum_5, sum_6, sum_7, user_id)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''', (sum_0, sum_1, sum_2, sum_3, sum_4, sum_5, sum_6, sum_7, user_id))
        self.db.commit()

    def fetch_ids100_sums(self, user_id):
        self.c.execute('''SELECT sum_0, sum_1, sum_2, sum_3, sum_4, sum_5, sum_6, sum_7
                            FROM ids100_sums WHERE user_id=?''', (user_id,))
        return self.c.fetchone()

    def fetch_ids100_question(self, index):
        self.c.execute('''SELECT question FROM ids100_questions WHERE id=?''', (index,))
        return self.c.fetchone()[0]

    def fetch_ids100_done_status(self, user_id):
        self.c.execute('''SELECT ids100_done FROM users WHERE id=?''', (user_id,))
        if (self.c.fetchone()[0] == 0):
            return False
        else:
            return True

    def drop_ids100_sums_and_answers(self):
        self.c.execute('''DELETE FROM ids100_answers''')
        self.c.execute('''DELETE FROM ids100_sums''')
        self.db.commit()

    def fetch_satisfaction_question(self, index):
        self.c.execute('''SELECT question FROM satisfaction_questions WHERE id=?''', (index,))
        return self.c.fetchone()[0]

    def push_satisfaction_question_value(self, question_id, user_id, answer):
        self.c.execute('''
            INSERT INTO satisfaction_answers(question_id, user_id, answer_value)
            VALUES(?, ?, ?)''', (question_id, user_id, answer))
        self.db.commit()

    def push_satisfaction_test_done(self, user_id):
        self.c.execute('''UPDATE users SET satisfaction_done=? WHERE id=?''', (1, user_id))
        self.db.commit()

    def fetch_satisfaction_done_status(self, user_id):
        self.c.execute('''SELECT satisfaction_done FROM users WHERE id=?''', (user_id,))
        if (self.c.fetchone()[0] == 0):
            return False
        else:
            return True

    def drop_satisfaction_answers(self):
        self.c.execute('''
            DELETE FROM satisfaction_answers
        ''')
        self.db.commit()
