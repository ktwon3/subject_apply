import random
import copy
import utill
import pickle

def apply(remain_subject, students, NOSD, nob, time = 30):
    students_num = [i for i in range(len(students))]
    result = [{} for _ in range(NOSD)]
    for _ in range(time):  # 1차에서는 time = 30으로도 충분한 것 같음
        random.shuffle(students_num)
        for num in students_num:
            c_b = list(result[num].keys())
            choosed_block = copy.deepcopy(c_b)
            for i in c_b:
                choosed_block = utill.add_overlab_block(i, c_b)
            if len(choosed_block) == nob : continue
            r = random.randrange(len(students[num].subject))
            sub = students[num].subject[r]
            class_list = list(remain_subject[sub].keys())  # 분반 리스트
            c = copy.deepcopy(class_list)
            for i in c:
                if remain_subject[sub][i][0] in choosed_block or remain_subject[sub][i][1] <= 0:
                        class_list.remove(i)
            if len(class_list) > 0 :
                r2 = random.choice(class_list)
                result[num][remain_subject[sub][r2][0]] = [sub, r2]  # {블럭 : [과목, 분반]}, 각 인덱스는 학생
                remain_subject[sub][r2][1] -= 1

    return result


def check_applying_result(a, nob):  # apply 이후 신청 성공한 블럭 블럭 몇갠지 return
    b = {}
    for i in range(1, nob + 1):
        b[i] = 0
    for i in range(len(a)):
        b[len(a[i].keys())] += 1
    return b


def find_block_student(resul,bloc_num):
    r = []
    for i in range(len(resul)):
        if bloc_num == len(resul[i].keys()):
            r.append(i)
    return r

if __name__ == '__main__':
    SPC = utill.SPC  # student per class, 분반당 학생수, 현재는 21로 고정
    NOSD = utill.NOSD  # Number Of StuDent, 총 학생수
    NOB = utill.NOB  # Number Of Block, 블럭 개수
    NOSJ = utill.NOSJ  # Number Of SubJect, 공강을 합친 과목 수
    remain_subject = utill.set_remain_subject()
    # remain_subject : 과목에 따른 남은 학생수, 한 딕셔너리 안에 하나의 과목, key는 분반, value는 [블럭, 남은 인원 수]

    with open('students.txt', 'rb') as f:
        students = pickle.load(f)

    r = copy.deepcopy(remain_subject)
    result = apply(r, students, NOSD, 1000)

    checked_dic = check_applying_result(result, NOB)
    print(checked_dic)