class Points:
    def __init__(self):
        self.unpleasant_feelings    = 0
        self.physical_discomfort    = 0
        self.pleasant_feelings      = 0
        self.test_personal_control  = 0
        self.temptations            = 0
        self.conflicts              = 0
        self.social_pressure        = 0
        self.pleasant_socialization = 0
        self.l_1 = ['1', '4', '11', '14', '21', '24', '31', '34', '41', '44', '51', '54', '61', '64', '71', '74', '81', '84', '91', '94']
        self.l_2 = ['2', '12', '22', '32', '42', '52', '62', '72', '82', '92']
        self.l_3 = ['3', '13', '23', '33', '43', '53', '63', '73', '83', '93']
        self.l_4 = ['5', '15', '25', '35', '45', '55', '65', '75', '85', '95']
        self.l_5 = ['6', '16', '26', '36', '46', '56', '66', '76', '86', '96']
        self.l_6 = ['7', '10', '17', '20', '27', '30', '37', '40', '47', '50', '57', '60', '67', '70', '77', '80', '87', '90', '97', '100']
        self.l_7 = ['8', '18', '28', '38', '48', '58', '68', '78', '88', '98']
        self.l_8 = ['9', '19', '29', '39', '49', '59', '69', '79', '89', '99']


    def calc_scale(self):
        s_1 = (self.unpleasant_feelings / 60) * 100
        s_2 = (self.physical_discomfort / 60) * 200
        s_3 = (self.pleasant_feelings / 60) * 200
        s_4 = (self.test_personal_control / 60) * 200
        s_5 = (self.temptations / 60) * 200
        s_6 = (self.conflicts / 60) * 100
        s_7 = (self.social_pressure / 60) * 200
        s_8 = (self.pleasant_socialization / 60) * 200
        total = [int(s_1), int(s_2), int(s_3), int(s_4), int(s_5), int(s_6), int(s_7), int(s_8)]
        #for i in range(len(total)):
        #    if (i == len(total)-1):
        #        total_str += str(total[i])
        #    else:
        #        total_str += str(total[i]) + ', '
        #self.print_to_file(total_str)
        return total

    # Takes question_count (index of question) and the value (user inputed) and calculates the sums
    def recieve_question(self, question_count, point):
        question_count = str(question_count)
        if question_count in self.l_1:
            self.unpleasant_feelings += point
        elif question_count in self.l_2:
            self.physical_discomfort += point
        elif question_count in self.l_3:
            self.pleasant_feelings += point
        elif question_count in self.l_4:
            self.test_personal_control += point
        elif question_count in self.l_5:
            self.temptations += point
        elif question_count in self.l_6:
            self.conflicts += point
        elif question_count in self.l_7:
            self.social_pressure += point
        else:
            self.pleasant_socialization += point

    def sort_high_rated_questions(self, high_rated_questions):
        #TODO: Sort high rated questions into easy accessed DS for displaying in "results"
        pass

    def return_test(self, count, point):
        return count, point

    def print_to_file(self, vals):
        f = open("testresult.txt", 'w')
        f.write(vals)
        f.close()