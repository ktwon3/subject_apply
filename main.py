import random
import utill, apply_subject
import pickle
import numpy as np
from basic_var import SPC, NOSD, NOB, NOSJ


class Analyze:
    def __init__(self):
        self.remain_subject = utill.set_remain_subject()
        with open('students.txt', 'rb') as f: self.students = pickle.load(f)

    def apply_count(self):
        result = apply_subject.apply(self.students, NOSD, NOB, 100)
        return np.array([len(dic) for dic in result])

    def repeat_apply(self, repeat):
        temp = np.zeros(NOSD)
        for i in range(repeat):
            temp += self.apply_count()
        return temp

    def calculate_weight(self, repeat):
        arr = self.repeat_apply(repeat)
        weight_arr = np.zeros(NOSJ)

        for i in range(NOSD):
            weight = arr[i]
            sub_list = self.students[i].subject
            for sub in sub_list:
                weight_arr[sub] += weight

        count_arr = np.array(list(self.count_sum.values()))
        self.mean_arr = weight_arr / count_arr



    def count_sum_subject(self):
        self.count_sum = {}
        for i in range(NOSJ):
            self.count_sum[i] = 0
        for student in self.students:
            sub_list = student.subject
            for sub in sub_list:
                self.count_sum[sub] += 1

    def main_loop(self, repeat):
        self.count_sum_subject()
        self.calculate_weight(repeat)
        return self.mean_arr



s = Analyze()
print(s.main_loop(100))