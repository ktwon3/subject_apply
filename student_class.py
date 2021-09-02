import apply_subject, utill
import random
from basic_var import SPC, NOSD, NOB, NOSJ

class Student:
    def __init__(self, subject):
        self.subject = subject
       
    def __repr__(self):
        return '<Student subject: ' + str(self.subject) + '>\n'

    def return_sub(self):
        return self.subject

    def set_apply_order(self, nosd, nob, probality=10):
        rs = utill.set_remain_subject()
        count = 0
        while True:
            count += 1
            apply_list = apply_subject.apply([self], nosd, nob, time=30)[0]
            if len(apply_list) == 10: break
        sub_list, class_num, all_list, result = [], [], [], {}
        for block in apply_list.keys():
            sub_list.append(apply_list[block][0])
            class_num.append(apply_list[block][1])
            all_list.append([block, apply_list[block][0], apply_list[block][1]])

        research_list = [i for i in range(31, 37)]
        sub_in_research = [i for i in sub_list if i in research_list]

        if len(sub_in_research) == 1:
            sub_in_research = sub_in_research[0]
            research_index = sub_list.index(sub_in_research)
            result[sub_list[research_index]] = class_num[research_index]
            # result = {1번째 신청할 과목: 분반, 2번째 신청할 과목: 분반 ...}

        count_fixed_sub = len([i for i in range(9) if random.randint(1, probality) == 1])
        not_resear_list = [i for i in sub_list if i not in research_list]
        fixed_sub_list = random.sample(not_resear_list, count_fixed_sub)
        fixed_index = [sub_list.index(i) for i in fixed_sub_list]
        for i in fixed_index:
            result[sub_list[i]] = class_num[i]

        non_fixed_list = [i for i in sub_list if i not in fixed_sub_list and i not in research_list]
        random.shuffle(non_fixed_list)
        non_fixed_index = [sub_list.index(i) for i in non_fixed_list]
        for i in non_fixed_index:
            result[sub_list[i]] = class_num[i]

        if len(result) != 10:
            raise Exception('10개 과목 적용 실패')

        if sub_in_research:
            self.count_fixed = count_fixed_sub + 1
        else:
            self.count_fixed = count_fixed_sub

        self.ideal_subject = result

    def apply(self, nosd, nob):
        self.apply_result = apply_subject.apply([self], nosd, nob, time=30, fix=True)[0]

    def check_result(self):
        ideal_sub_list = [i for i in self.ideal_subject.keys()]
        apply_sub_list = [self.apply_result[i][0] for i in self.apply_result.keys()]

        same = 0
        for i in range(len(apply_sub_list)):
            same = i
            if ideal_sub_list[i] != apply_sub_list[i]: break

        if self.count_fixed > same:
            self.fix_same = same

        else:
            self.fix_same = self.count_fixed

        return self.count_fixed - self.fix_same




if __name__ == "__main__":
    import pickle
    SPC = utill.SPC  # student per class, 분반당 학생수, 현재는 21로 고정
    NOSD = utill.NOSD  # Number Of StuDent, 총 학생수
    NOB = utill.NOB  # Number Of Block, 블럭 개수
    NOSJ = utill.NOSJ  # Number Of SubJect, 공강을 합친 과목 수
    remain_subject = utill.set_remain_subject()
    # remain_subject : 과목에 따른 남은 학생수, 한 딕셔너리 안에 하나의 과목, key는 분반, value는 [블럭, 남은 인원 수]

    with open('students.txt', 'rb') as f:
        students = pickle.load(f)
    for s in students:
        r = s.set_apply_order(NOSD, NOB)
    sum_ = 0
    for s in students:
        s.apply(NOSD,NOB)
        a = s.check_result()
        if a == 0: sum_ += 1
    print(sum_)


    #apply_subject.frm_print(10, 10, students, True)
    result = apply_subject.apply(students, NOSD, NOB, 30, True)
    print(result)




