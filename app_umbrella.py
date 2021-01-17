import app_users, app_super, app_inst, app_utils

class AppUmbrella():

    def __init__(self):
        self.users = app_users.AppUsers()
        self.supers = app_super.AppSuper()
        self.utils = app_utils.AppUtils()
        self.inst = app_inst.AppInst()

    # Create the full social_tests.db with all it's required tables
    def init_full_db(self):
        self.users.init_users_table()
        self.supers.init_supervisors_table()
        self.utils.init_ids100_answer_table()
        self.utils.init_ids100_sums()
        self.utils.init_ids100_questions_table()
        self.users.init_user_requests_table()
        self.utils.init_satisfaction_scale_questions()
        self.utils.init_satisfaction_answers()
        self.inst.init_institution_table()
        self.supers.init_super_requests_table()

    def push_tests_inst_super(self):
        self.inst.push_test_institutions()
        self.supers.push_test_supervisors()

    def push_test_users(self):
        self.users.push_test_users()
        users = self.users.fetch_user_id_by_group_key(1)
        for i in range(len(users)):
            self.users.push_user_reg_request(users[i][0], 1)


a = AppUmbrella()
a.init_full_db()
a.push_tests_inst_super()
#a.push_test_users()