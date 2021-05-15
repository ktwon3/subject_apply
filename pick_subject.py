import copy
import random
import pickle
import student_class

def pick(remain_subject, NOSJ, NOSD, NOB, Student, save = False):
    tryCount = 0
    rs_ = [0] * len(remain_subject)
    for i in range(len(remain_subject)):
        a = list(remain_subject[i].values())
        for j in a:
            rs_[i] += j[1]  # rs_는 과목당 듣는 학생수, (분반) * (분반당 학생수)의 총합
    while True:
        tryCount += 1
        switch = True
        students = []
        rs = copy.deepcopy(rs_)  # rs는 과목 배정을 위한 것, deepcopy는 변수간 영향 x
        for n in range(NOSD):
            choosed_subject = []
            choosed_block = []  # 블럭을 고려해줘야 구조적으로 불가능한 시간표가 나오지 않음, 다만 배정시 고려는 x
            s = [i for i in range(NOSJ)]  # s는 과목 번호
            random.shuffle(s)
            for i in s:
                if rs[i] <= 0:
                    continue
                else:
                    for j in remain_subject[i].keys():
                        if remain_subject[i][j][0] in choosed_block: continue
                        else:
                            choosed_subject.append(i)
                            choosed_block.append(remain_subject[i][j][0])
                            rs[i] -= 1
                            break
                if len(choosed_subject) >= 6: break
            if len(choosed_subject) != NOB:
                if n >= 200 : print(str(tryCount) + '번째 시도: ' + str(n) + '번째 학생 실패')
                print(rs)
                print(choosed_block)
                print(choosed_subject)
                print('=' * 100)
                switch = False
                break
            students.append(Student(choosed_subject))
            if not switch: break
        if switch: break
    if save:
        with open('students.txt', 'wb') as f:
            pickle.dump(students, f)
    return students


def apply(remain_subject, students, NOSD, time = 30):
    students_num = [i for i in range(len(students))]
    result = [{} for _ in range(NOSD)]
    for _ in range(time):  # 1차에서는 time = 30으로도 충분한 것 같음
        random.shuffle(students_num)
        for num in students_num:
            choosed_block = list(result[num].keys())
            if len(choosed_block) == 6 : continue
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


if __name__ == '__main__':
    SPC = student_class.SPC   # student per class, 분반당 학생수, 현재는 21로 고정
    NOSD = student_class.NOSD  # Number Of StuDent, 총 학생수
    NOB = student_class.NOB  # Number Of Block, 블럭 개수
    NOSJ = student_class.NOSJ  # Number Of SubJect, 공강을 합친 과목 수

    with open("subject_block.txt", "r") as f:
        subject_block = f.read().splitlines()  # subject_block : 한 과목이 어떤 블록에 해당되는지 정리

    remain_subject = []
    # remain_subject : 과목에 따른 남은 학생수, 한 딕셔너리 안에 하나의 과목, key는 분반, value는 [블럭, 남은 인원 수]

    for i in range(len(subject_block)):
        temp = {}
        nums = subject_block[i].split()  # nums : subject_block의 각각의 숫자 분리
        for i in range(len(nums)):
            temp[i+1] = [int(nums[i]) - 1, SPC]
        remain_subject.append(temp)

    remain_subject[0] = {1: [4, NOSD], 2: [5, NOSD]}  # 공강 조정
    temp = pick(remain_subject, NOSJ, NOSD, NOB, student_class.Student, save = True)
    print(remain_subject)
    for i in temp:
        print(i.subject)
