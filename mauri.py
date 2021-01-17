from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.animation import Animation
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
import app_users, app_super, app_utils, app_inst
import datetime
from kivy.clock import Clock
from ids_points import Points
import random
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.list import TwoLineListItem



class UserLogin(Screen):
    def __init__(self, **kwargs):
        super(UserLogin, self).__init__(**kwargs)
        self.sql_cursor_user = app_users.AppUsers()

    # self.screen.ids.text_field_error.error = True
    def anim_card(self, widget):
        anim = Animation(opacity=1)
        anim.start(widget)

    def goto_superlogin(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "superlogin"


    # Handle login request
    def login(self):
        if(self.check_email() and self.check_password() and self.check_acc_value()):
            self.manager.get_screen("userhome").user_id = self.sql_cursor_user.fetch_user_id_by_email(self.ids["email"].text)
            self.manager.current = "userhome"
        else:
            pass

    # Check Pwd field and content against database
    def check_password(self):

        if(self.ids["pwd"].text == ''):
            return False
        elif(self.sql_cursor_user.fetch_user_email_pwd(self.ids["email"].text.lower())[1] != self.ids["pwd"].text):
            toast("Lösenordet och email matchade inte")
        else:
            return True

    def check_acc_value(self):
        user_id = self.sql_cursor_user.fetch_user_id_by_email(self.ids["email"].text)
        acc_value = self.sql_cursor_user.fetch_user_acc_value(user_id)
        if(acc_value == -1):
            toast("Din registreringsförfrågan har inte blivit godkänd ännu")
            return False
        else:
            return True



    # Check Email Field and against database
    def check_email(self):

        if(self.ids["email"].text == ''):
            return False
        elif(self.sql_cursor_user.check_email_availability(self.ids["email"].text.lower())):
            toast("Email är inte registrerad")
            return False
        else:
            return True

class SuperLogin(Screen):

    def __init__(self, **kwargs):
        super(SuperLogin, self).__init__(**kwargs)
        self.sql_cursor_super = app_super.AppSuper()

    def goto_userlogin(self, *args):
        self.manager.transition.direction = "right"
        self.manager.current = "userlogin"


    # Handle login request
    def login(self):
        if(self.check_email() and self.check_password()):
            super_id = self.sql_cursor_super.fetch_super_id_by_email(self.ids["email"].text)
            self.manager.get_screen("superhome").super_id = super_id
            self.manager.get_screen("superhome").group_key = self.sql_cursor_super.fetch_super_group_key_by_id(super_id)
            self.manager.transition.direction = "left"
            self.manager.current = "superhome"
        else:
            pass

    # Check Pwd field and content against database
    def check_password(self):
        if(self.ids["pwd"].text == ''):
            return False
        elif(self.sql_cursor_super.fetch_super_email_pwd(self.ids["email"].text.lower())[1] != self.ids["pwd"].text):
            toast("Lösenordet och email matchade inte")
        else:
            return True


    # Check Email Field and against database
    def check_email(self):
        if(self.ids["email"].text == ''):
            return False
        elif(self.sql_cursor_super.check_super_email_availability(self.ids["email"].text.lower())):
            toast("Email är inte registrerad")
            return False
        else:
            return True

class RegisterUser(Screen):

    def __init__(self, **kwargs):
        super(RegisterUser, self).__init__(**kwargs)
        self.sql_cursor_user = app_users.AppUsers()
        self.sql_cursor_inst = app_inst.AppInst()
        self.all_inst = self.sql_cursor_inst.fetch_all_institutions()
        self.selected_inst = None
        self.selected_sex = None
        self.acc_key = 0
        self.date = int(str(datetime.datetime.now().date()).replace("-", ""))

    def callback_for_inst_items(self, *args):
        toast(args[0])
        self.ids["inst_label"].text = args[0]
        self.selected_inst = args[1]
        print(self.selected_inst)


    def show_institutions(self):
        bottom_sheet_menu = MDListBottomSheet()
        for i in range(len(self.all_inst)):
            bottom_sheet_menu.add_item(
                self.all_inst[i][1].capitalize() + " (" + self.all_inst[i][2] + ")",
                lambda x, y=i: self.callback_for_inst_items(
                    self.all_inst[y][1].capitalize() + " (" + self.all_inst[y][2] + ")", self.all_inst[y][0]
                ),
            )
        bottom_sheet_menu.open()

    def callback_for_sexes_items(self, *args):
        self.ids["sex_label"].text = args[0]
        self.selected_sex = args[1]
        print(self.selected_sex)


    def show_sexes(self):
        bottom_sheet_menu = MDListBottomSheet()
        sex = ["Man", "Kvinna", "Annat"]
        for i in range(3):
            bottom_sheet_menu.add_item(
                sex[i],
                lambda x, y=i: self.callback_for_sexes_items(
                    sex[y], y
                ),
            )
        bottom_sheet_menu.open()


    def anim_to_next(self, card_1, card_2):
        if(self.check_inst() and self.check_sex() and self.check_name() and self.check_surname()):
            anim_1_1 = Animation(opacity=0,duration=0.3)
            anim_1 = Animation(pos_hint={"center_x": -0.5},duration=0.5)
            anim_2 = Animation(pos_hint={"center_x": 0.5},duration=0.5)
            anim_1_1.start(card_1)
            anim_1.start(card_1)
            anim_2.start(card_2)
        else:
            toast("Vänligen fyll i alla fälten")

    def goto_userlogin(self):
        self.manager.transition.direction = "right"
        self.manager.current = "userlogin"

    def register_user(self):
        if(self.check_email() and self.check_pwd() and self.check_sex() and self.check_age() and self.check_inst() and self.check_name() and self.check_surname()):
            self.sql_cursor_user.add_user(self.ids["name"].text, self.ids["surname"].text, self.ids["email"].text,
                                     self.ids["age"].text, self.selected_sex, self.date,
                                     self.selected_inst, self.ids["pwd"].text)
            # name, surname, email, age, sex, reg_date, group_key, password
            user_id = self.sql_cursor_user.fetch_user_id_by_email(self.ids["email"].text)
            self.sql_cursor_user.push_user_reg_request(user_id, self.selected_inst)
            self.manager.current = "userlogin"
        else:
            pass

    def check_name(self):
        if(self.ids["name"].text == ""):
            return False
        elif(not self.ids["name"].text.isalpha()):
            return False
        else:
            return True

    def check_surname(self):
        if(self.ids["surname"].text == ""):
            return False
        elif(not self.ids["surname"].text.isalpha()):
            return False
        else:
            return True

    # Check so that email is correctly entered and does not exist in database
    def check_email(self):
        if(self.ids["email"].text == ''):
            return False
        elif ('@' not in self.ids["email"].text):
            toast("Email är inte godkänd")
            return False
        elif(not self.sql_cursor_user.check_email_availability(self.ids["email"].text.lower())):
            toast("Email är redan registrerad")
            return False
        else:
            return True

    # Check password
    def check_pwd(self):
        if(self.ids["pwd"].text == ''):
            return False
        elif(self.ids["pwd_conf"].text == ''):
            return False
        elif(len(self.ids["pwd"].text) < 6):
            toast("Lösenordet är för kort\nVänligen använd 6 eller fler tecken")
            return False
        elif(not (self.ids["pwd"].text == self.ids["pwd_conf"].text)):
            toast("Lösenorden överrensstämmer inte")
            return False
        else:
            return True

    # Check so that sex is marked
    def check_sex(self):
        if(self.selected_sex == None):
            toast("Du har inte markerat vilket kön\nDu identifierar dig med")
            return False
        else:
            return True
    # Check that age is over 12, start value: 11
    def check_age(self):
        if(self.ids["age"].text == ""):
            return False
        else:
            return True

    def check_inst(self):
        if(self.selected_inst == None):
            toast("Vänligen välj rätt instutition")
            return False
        else:
            return True

class RegisterSupervisor(Screen):

    def __init__(self, **kwargs):
        super(RegisterSupervisor, self).__init__()
        self.sql_cursor_super = app_users.AppUsers()
        self.sql_cursor_inst = app_inst.AppInst()
        self.all_inst = self.sql_cursor_inst.fetch_all_institutions()
        self.selected_inst = None
        self.acc_key = 1
        self.date = int(str(datetime.datetime.now().date()).replace("-", ""))

    def callback_for_inst_items(self, *args):
        toast(args[0])
        self.ids["inst_label"].text = args[0]
        self.selected_inst = args[1]
        print(self.selected_inst)

    def show_institutions(self):
        bottom_sheet_menu = MDListBottomSheet()
        for i in range(len(self.all_inst)):
            bottom_sheet_menu.add_item(
                self.all_inst[i][1].capitalize() + " (" + self.all_inst[i][2] + ")",
                lambda x, y=i: self.callback_for_inst_items(
                    self.all_inst[y][1].capitalize() + " (" + self.all_inst[y][2] + ")", self.all_inst[y][0]
                ),
            )
        bottom_sheet_menu.open()

    def anim_to_next(self, card_1, card_2):
        if(self.check_name() and self.check_surname() and self.check_inst()):
            anim_1_1 = Animation(opacity=0, duration=0.3)
            anim_1 = Animation(pos_hint={"center_x": -0.5}, duration=0.5)
            anim_2 = Animation(pos_hint={"center_x": 0.5}, duration=0.5)
            anim_1_1.start(card_1)
            anim_1.start(card_1)
            anim_2.start(card_2)
        else:
            toast("Vänligen fyll i alla fälten")

    def goto_superlogin(self):
        self.manager.transition.direction = "right"
        self.manager.current = "superlogin"


    def check_pwd(self):
        if(self.ids["pwd"].text == ''):
            return False
        elif(self.ids["pwd_conf"].text == ''):
            return False
        elif(len(self.ids["pwd"].text) < 6):
            toast("Lösenordet är för kort\nVänligen använd 6 eller fler tecken")
            return False
        elif(not (self.ids["pwd"].text == self.ids["pwd_conf"].text)):
            toast("Lösenorden överrensstämmer inte")
            return False
        else:
            return True

    def check_email(self):
        if (self.ids["email"].text == ''):
            return False
        elif ('@' not in self.ids["email"].text):
            toast("Email är inte godkänd")
            return False
        elif (not self.sql_cursor_super.check_super_email_availability(self.ids["email"].text.lower())):
            toast("Email är redan registrerad")
            return False
        else:
            return True

    def check_name(self):
        if(self.ids["name"].text == ""):
            return False
        elif(not self.ids["name"].text.isalpha()):
            return False
        else:
            return True

    def check_surname(self):
        if(self.ids["surname"].text == ""):
            return False
        elif(not self.ids["surname"].text.isalpha()):
            return False
        else:
            return True

    def check_inst(self):
        if(self.selected_inst == None):
            toast("Vänligen välj rätt instutition")
            return False
        else:
            return True

    def register_super(self):
        if(self.check_name() and self.check_surname() and self.check_inst() and self.check_email() and self.check_pwd()):
            self.sql_cursor_super.add_supervisor(self.ids["name"].text, self.ids["surname"].text, self.ids["email"].text,
                                           self.date, self.selected_inst, self.ids["pwd"].text)
            self.manager.transition.direction = "right"
            self.manager.current = "superlogin"
        else:
            pass

class UserHome(Screen):

    def __init__(self, **kwargs):
        super(UserHome, self).__init__(**kwargs)
        self.user_id = None

    def goto_userhome(self):
        self.manager.transition.direction = "right"
        self.manager.current = "userhome"

    def goto_logout(self):
        self.user_id = None
        self.manager.transition.direction = "right"
        self.manager.current = "userlogin"

class SuperHome(Screen):

    def __init__(self, **kwargs):
        super(SuperHome, self).__init__(**kwargs)
        self.super_id = None
        self.group_key = None

    def goto_logout(self):
        self.super_id = None
        self.manager.transition.direction = "right"
        self.manager.current = "superlogin"

class SuperRequests(Screen):

    def __init__(self, **kwargs):
        super(SuperRequests, self).__init__(**kwargs)
        self.all_reg_requests = None
        self.sql_cursor_user = app_users.AppUsers()
        self.current_user_id = None

    def on_enter(self, *args):
        self.show_requests()

    def show_requests(self):
        self.all_requests = self.sql_cursor_user.fetch_user_reg_requests(self.manager.get_screen("superhome").group_key)
        for i in range(len(self.all_requests)):
            user_id = self.all_requests[i][0]
            user = self.sql_cursor_user.fetch_user_info_by_id(user_id)
            name = user[0]
            surname = user[1]
            email = user[2]
            age = user[3]
            sex = ""
            if(user[4] == 0):
                sex = "Man"
            elif(user[4] == 1):
                sex = "Kvinna"
            else:
                sex = "Annat"
            reg_date = user[5]
            self.ids.users_list.add_widget(

                ThreeLineListItem(id=str(user_id), text= "Acceptera Registrering: " + name.capitalize() + " " + surname.capitalize(),
                                secondary_text = email + ", Ålder: " + str(age) + ", Kön: " + sex ,
                                tertiary_text = "Förfrågan inkommen: " + str(reg_date), on_release=self.accept_or_deny_request)

            )

    def accept_or_deny_request(self, instance):
        self.current_user_id = instance.id
        user = self.sql_cursor_user.fetch_user_info_by_id(instance.id)
        name = user[0].capitalize()
        surname = user[1].capitalize()
        email = user[2]
        age = str(user[3])

        self.ids["name"].text = name
        self.ids["surname"].text = surname
        self.ids["age"].text =  age
        self.ids["email"].text = email
        anim_1_1 = Animation(opacity=0, duration=0.3)
        anim_1 = Animation(pos_hint={"center_x": -0.5}, duration=0.5)
        anim_2 = Animation(pos_hint={"center_x": 0.5}, duration=0.5)
        anim_1_1.start(self.ids["card_requests"])
        anim_1.start(self.ids["card_requests"])
        anim_2.start(self.ids["card_acc_spec_req"])
        self.ids.card_acc_spec_req.opacity = 1
        self.current_user_id = instance.id

    def back_to_rerquests(self):
        self.ids.users_list.clear_widgets()
        anim_1_1 = Animation(opacity=0, duration=0.3)
        anim_2_1 = Animation(opacity=1, duration= 0.6)
        anim_1 = Animation(pos_hint={"center_x": -0.5}, duration=0.5)
        anim_2 = Animation(pos_hint={"center_x": 0.5}, duration=0.5)
        anim_1_1.start(self.ids["card_acc_spec_req"])
        anim_1.start(self.ids["card_acc_spec_req"])
        anim_2_1.start(self.ids["card_requests"])
        anim_2.start(self.ids["card_requests"])
        self.show_requests()
        
    def accept_user(self):
        user = self.sql_cursor_user.fetch_user_info_by_id(self.current_user_id)
        name = user[0].capitalize()
        surname = user[1].capitalize()
        self.sql_cursor_user.push_user_acc_value_zero(self.current_user_id)
        self.sql_cursor_user.drop_user_reg_request(self.current_user_id)
        toast(name + " " + surname + " är nu tillagd")
        self.back_to_rerquests()

    def deny_user(self):
        user = self.sql_cursor_user.fetch_user_info_by_id(self.current_user_id)
        name = user[0]
        surname = user[1]
        self.sql_cursor_user.drop_user_reg_request(self.current_user_id)
        self.sql_cursor_user.drop_user(self.current_user_id)
        toast(name + " " + surname + " är nekad åtkomst")
        self.back_to_rerquests()

    def goto_logout(self):
        self.manager.get_screen("superhome").super_id = None
        self.manager.transition.direction = "right"
        self.manager.current = "superlogin"

    def goto_superhome(self):
        self.manager.transition.direction = "right"
        self.manager.current = "superhome"

class UserForms(Screen):

    def __init__(self, **kwargs):
        super(UserForms, self).__init__(**kwargs)
        self.item_queue = [1, 2, 3]
        self.counter = 1
        self.pos_itm = 0.1
        self.sql_cursor_user = app_users.AppUsers()
        self.sql_cursor_utils = app_utils.AppUtils()
        self.user_id = None
        self.ids_done_status = None

    def on_enter(self, *args):
        self.user_id = self.manager.get_screen("userhome").user_id
        self.ids_done_status = self.sql_cursor_utils.fetch_ids100_done_status(self.user_id)
        if(self.ids_done_status == 1):
            self.ids["ids_100_icon"].source = "check_icon.png"
        else:
            pass
        Clock.schedule_interval(lambda dt: self.itm_anim(), 0.5)


    def itm_anim(self):
        itm = "itm_"+str(self.counter)

        if(self.counter > len(self.item_queue)):
            Clock.unschedule(True)
        else:
            anim_op = Animation(opacity=1, duration=0.8)
            anim_stack_1 = Animation(pos_hint = {"center_y": self.pos_itm}, duration=0.5)
            anim_op.start(self.ids[itm])
            anim_stack_1.start(self.ids[itm])
            self.counter += 1
            self.pos_itm += 0.15

    def goto_userhome(self):
        self.manager.transition.direction = "right"
        self.manager.current = "userhome"

    def goto_logout(self):
        self.manager.get_screen("userhome").user_id = None
        self.manager.transition.direction = "right"
        self.manager.current = "userlogin"

class Ids100Form(Screen):

    def __init__(self, **kwargs):
        super(Ids100Form, self).__init__(**kwargs)
        self.counter = 0
        self.sql_cursor_user = app_users.AppUsers()
        self.sql_cursor_utils = app_utils.AppUtils()
        self.active_check = None
        self.points_cursor = Points()
        # TODO: display high rated questions when bars is tapped
        self.high_rated_questions = []
        self.user_id = None


    # IF IDS100_DONE = 1, GO DIRECTLY TO RESULTS
    def on_enter(self):
        self.user_id = self.manager.get_screen("userhome").user_id
        self.ids100_done = self.sql_cursor_utils.fetch_ids100_done_status(self.user_id)
        if (self.ids100_done == 1):
            self.goto_ids100_results()
        else:
            pass

    def goto_ids100_results(self):
        self.manager.current = "ids100results"

    # called when user presses "next" button
    def next_question(self):
        if (self.counter < 1):
            self.counter += 1
            self.active_check = None
            self.ids["question_label"].text = self.sql_cursor_utils.fetch_ids100_question(self.counter)
        elif (self.counter >= 1 and self.counter <= 100 and self.active_check != None):
            self.sql_cursor_utils.push_ids100_question_value(self.counter, self.user_id, int(self.active_check))
            self.counter += 1

            for i in range(4):
                self.ids["chk_" + str(i)].active = False

            if (self.counter <= 100):
                self.ids["question_label"].text = self.sql_cursor_utils.fetch_ids100_question(self.counter)
            else:
                self.calc_and_push_results()
            self.active_check = None
        else:
            pass

    # Called when all questions have been answered
    def calc_and_push_results(self):

        self.sql_cursor_utils.push_ids100_test_done(self.user_id)
        values = self.sql_cursor_utils.fetch_ids100_user_answers(self.user_id)

        for i in range(len(values)):
            self.points_cursor.recieve_question(i + 1, values[i][1])
            if (values[i][1] > 2):
                self.high_rated_questions.append(i + 1)
            else:
                pass

        sums = self.points_cursor.calc_scale()
        self.sql_cursor_utils.push_ids100_sums(sums[0], sums[1], sums[2], sums[3], sums[4], sums[5], sums[6], sums[7],
                                         self.user_id)
        self.sql_cursor_user.push_user_points_by_id(20, self.user_id)
        self.manager.current = "ids100results"

    def autofill_questions(self):
        counter = 1
        while (counter <= 100):
            self.sql_cursor_utils.push_ids100_question_value(counter, self.manager.get_screen("userhome").user_id,
                                                      random.randint(0, 3))
            counter += 1
        if (counter == 101):
            self.calc_and_push_results()
        else:
            pass

class Ids100Results(Screen):

    def on_enter(self, *args):
        self.values_y = None
        self.sql_cursor_utils = app_utils.AppUtils()
        self.user_id = self.manager.get_screen("userhome").user_id
        self.show_results()

    def goto_userhome(self):
        self.manager.transition.direction = "right"
        self.manager.current = "userhome"

    def goto_logout(self):
        self.manager.get_screen("userhome").user_id = None
        self.manager.transition.direction = "right"
        self.manager.current = "userlogin"

    def show_results(self):
        self.get_ids100_sums()
        self.paint_labels()
        self.paint_bars()


    # Paints the different bars by using the calculated sums from ids100_sums table
    def paint_bars(self):
        for i in range(8):
            color_values = [0, 0, 0, 0]
            if (self.values_y[i] <= 10):
                color_values[0] = 0
                color_values[1] = 0.8
                color_values[2] = 0.1
                color_values[3] = self.values_y[i]/100
            elif (self.values_y[i] > 10 and self.values_y[i] <= 30):
                color_values[0] = 0.2
                color_values[1] = 0.6
                color_values[2] = 0
                color_values[3] = self.values_y[i]/100
            elif (self.values_y[i] > 30 and self.values_y[i] <= 50):
                color_values[0] = 0.5
                color_values[1] = 0.4
                color_values[2] = 0.1
                color_values[3] = self.values_y[i]/100
            else:
                color_values[0] = 1
                color_values[1] = 0
                color_values[2] = 0
                color_values[3] = self.values_y[i]/100

            self.ids["btn" + str(i)].size_hint = (1, self.values_y[i] / 100)
            self.ids["btn"+str(i)].background_color = (color_values[0], color_values[1], color_values[2], color_values[3])

    # Marks the bars with labels
    def paint_labels(self):
        labels = ['Obehagliga Känslor', 'Fysiskt Obehag', 'Behagliga Känslor',
                  'Testande av Personlig Kontroll', 'Frestelser', 'Konflikter', 'Social Press',
                  'Trevlig Samvaro']
        for i in range(len(labels)):
            self.ids["l"+str(i)].text = labels[i] + '\n' + '(' + str(self.values_y[i]) + ')'


    # Fetches the calculated sums from ids100_sums table in the db using the user_id
    # puts them into values_y
    def get_ids100_sums(self):
        self.values_y = self.sql_cursor_utils.fetch_ids100_sums(self.user_id)

class SatisfactionScale(Screen):
    pass

class SuperPushReq(Screen):

    def __init__(self, **kwargs):
        super(SuperPushReq, self).__init__(**kwargs)
        self.super_id = None
        self.group_key = None
        self.sql_cursor_super = app_super.AppSuper()
        self.sql_cursor_user = app_users.AppUsers()
        self.current_user = None
        self.current_name = None
        self.current_surname = None


    def on_enter(self):
        self.super_id = self.manager.get_screen("superhome").super_id
        self.group_key = self.manager.get_screen("superhome").group_key
        self.group_key = self.sql_cursor_super.fetch_super_group_key_by_id(self.super_id)
        self.all_users = self.sql_cursor_user.fetch_user_id_by_group_key(self.group_key)
        for i in range(len(self.all_users)):
            user_id = self.all_users[i][0]
            user = self.sql_cursor_user.fetch_user_info_by_id(user_id)
            name = user[0]
            surname = user[1]
            email = user[2]
            age = user[3]
            sex = ""
            if(user[4] == 0):
                sex = "Man"
            elif(user[4] == 1):
                sex = "Kvinna"
            else:
                sex = "Annat"
            self.ids.list_users.add_widget(

                TwoLineListItem(id=str(user_id), text= "Användare: " + name.capitalize() + " " + surname.capitalize(),
                                secondary_text = email + ", Ålder: " + str(age) + ", Kön: " + sex ,
                                on_release=self.push_request_screen)

            )

    def push_request_screen(self, instance):
        self.current_user = instance.id
        self.current_name = self.sql_cursor_user.fetch_user_info_by_id(instance.id)[0].capitalize()
        self.current_surname = self.sql_cursor_user.fetch_user_info_by_id(instance.id)[1].capitalize()
        self.ids["user_label"].text = "Skicka uppgift till:\n" + self.current_name + " " + self.current_surname

        anim_1_1 = Animation(opacity=0, duration=0.3)
        anim_1 = Animation(pos_hint={"center_x": -0.5}, duration=0.5)
        anim_2 = Animation(pos_hint={"center_x": 0.5}, duration=0.5)
        anim_1_1.start(self.ids["card_users"])
        anim_1.start(self.ids["card_users"])
        anim_2.start(self.ids["card_spec_user"])

    def push_req_ids_100(self):
        #self.sql_cursor.push_super_request(self.super_id).super_id, self.current_user, self.group_key, 0)
        self.ids["ids_icon"].icon = "check"
        toast("Uppgift 'IDS-100' skickad till:\n" + self.current_name + " " + self.current_surname)

    def push_req_satis(self):
        #self.sql_cursor.push_super_request(self.super_id).super_id, self.current_user, self.group_key, 1)
        self.ids["satis_icon"].icon = "check"
        toast("Uppgift 'Tillfredsskalan' skickad till:\n" + self.current_name + " " + self.current_surname)


    def goto_logout(self):
        self.manager.get_screen("superhome").super_id = None
        self.manager.get_screen("superhome").group_key = None
        self.manager.transition.direction = "right"
        self.manager.current = "superlogin"

class WinManager(ScreenManager):
    pass

class ReturnMauri(MDApp):
    Window.size = (480, 853)
    def build(self):
        sm = WinManager()
        sm.add_widget(UserLogin())
        sm.add_widget(SuperPushReq())
        sm.add_widget(SuperRequests())
        sm.add_widget(SuperLogin())
        sm.add_widget(UserForms())
        sm.add_widget(Ids100Form())
        sm.add_widget(Ids100Results())
        sm.add_widget(SatisfactionScale())
        sm.add_widget(UserHome())
        sm.add_widget(RegisterUser())
        sm.add_widget(SuperHome())
        sm.add_widget(RegisterSupervisor())

        return sm


if __name__ == '__main__':
    ReturnMauri().run()