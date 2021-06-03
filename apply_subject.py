import random
import copy
import utill
import pickle


def apply(remain_sub, stud, nosd, nob, time=30):
    re_sub = copy.deepcopy(remain_sub)
    students_num = [i for i in range(len(stud))]
    result_ = [{} for _ in range(nosd)]
    for _ in range(time):  # 1차에서는 time = 30으로도 충분한 것 같음
        random.shuffle(students_num)
        for num in students_num:
            c_b = list(result_[num].keys())
            chose_block = copy.deepcopy(c_b)
            if len(chose_block) == nob:
                continue
            for i in c_b:
                    chose_block = utill.add_overlap_block(i, c_b)

            ran = random.randrange(len(stud[num].subject))
            sub = stud[num].subject[ran]
            class_list = list(re_sub[sub].keys())  # 분반 리스트
            c = copy.deepcopy(class_list)
            for i in c:
                if re_sub[sub][i][0] in chose_block or re_sub[sub][i][1] <= 0:
                    class_list.remove(i)
            if len(class_list) > 0:
                r2 = random.choice(class_list)
                result_[num][re_sub[sub][r2][0]] = [sub, r2]  # {블럭 : [과목, 분반]}, 각 인덱스는 학생
                re_sub[sub][r2][1] -= 1

    return result_


def check_applying_result(a, nob):  # apply 이후 신청 성공한 블럭 블럭 몇갠지 return
    b = {}
    for i in range(nob + 1):
        b[i] = 0
    for i in range(len(a)):
        b[len(a[i].keys())] += 1
    return b


def find_block_student(resul, bloc_num):
    r_ = []
    for i in range(len(resul)):
        if bloc_num == len(resul[i].keys()):
            r_.append(i)
    return r_


def repeat_find_block_student(bloc_num, time, remain_subject, students):
    r = [0] * NOSD
    for _ in range(time):
        result = apply(remain_subject, students, NOSD, NOB, 30)

        # checked_dic = check_applying_result(result, NOB)
        # print(checked_dic)
        f_ = find_block_student(result, bloc_num)
        for n in f_:
            r[n] += 1
        if _ % (time/10) == 0: print('@', end = '')
    print()
    return r


def find_repeating_max(bloc_num, time, remain_subject, students):
    l = repeat_find_block_student(bloc_num, time, remain_subject, students)
    x, n = max(l), min(l)
    result = {'max': [], 'min': [], 'num': (x,n)}
    result['max'] = [i for i, value in enumerate(l) if value == x]
    result['min'] = [i for i, value in enumerate(l) if value == n]
    return result


def frm_print(block_num, time, remain_subject, students):
    r = find_repeating_max(block_num, time, remain_subject, students)
    print('최댓값 :', r['num'][0])
    for i in r['max']:
        print(str(i) + '학생 :', students[i].return_sub())
    print('최솟값 :', r['num'][1])
    for i in r['min']:
        print(str(i) + '학생 :', students[i].return_sub())


if __name__ == '__main__':
    SPC = utill.SPC  # student per class, 분반당 학생수, 현재는 21로 고정
    NOSD = utill.NOSD  # Number Of StuDent, 총 학생수
    NOB = utill.NOB  # Number Of Block, 블럭 개수
    NOSJ = utill.NOSJ  # Number Of SubJect, 공강을 합친 과목 수
    remain_subject = utill.set_remain_subject()
    # remain_subject : 과목에 따른 남은 학생수, 한 딕셔너리 안에 하나의 과목, key는 분반, value는 [블럭, 남은 인원 수]

    with open('students.txt', 'rb') as f:
        students = pickle.load(f)

    result = apply(remain_subject, students, NOSD, NOB, 100)
    checked_dic = check_applying_result(result, NOB)
    print(checked_dic)
    print(result)

    # print(repeat_find_block_student(9,100))
    frm_print(9, 10, remain_subject, students)
