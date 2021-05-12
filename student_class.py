import pickle
import pick_subject
import copy

class Student:
    def __init__(self, subject):
        self.subject = subject

def check_applying_result(a):
    b = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for i in range(len(a)):
        b[len(a[i].keys())] += 1
    return b

def set_remain_subject(sub_block):
    remain_subject = []

    for i in range(len(sub_block)):
        temp = {}
        nums = sub_block[i].split()  # nums : subject_block의 각각의 숫자 분리
        for i in range(len(nums)):
            temp[i + 1] = [int(nums[i]) - 1, SPC]
        remain_subject.append(temp)

    remain_subject[0] = {1: [4, NOSD], 2: [5, NOSD]}  # 공강 조정

    return remain_subject

SPC = 21  # student per class, 분반당 학생수, 현재는 21로 고정
NOSD = 204 # Number Of StuDent, 총 학생수
NOB = 6  # Number Of Block, 블럭 개수
NOSJ = 25 # Number Of SubJect, 공강을 합친 과목 수

if __name__ == '__main__':
    with open("subject_block.txt", "r") as f:
        subject_block = f.read().splitlines()  # subject_block : 한 과목이 어떤 블록에 해당되는지 정리

    remain_subject = set_remain_subject(subject_block)
    # remain_subject : 과목에 따른 남은 학생수, 한 딕셔너리 안에 하나의 과목, key는 분반, value는 [블럭, 남은 인원 수]

    with open('students.txt', 'rb') as f:
        students = pickle.load(f)

    r = copy.deepcopy(remain_subject)
    result = pick_subject.apply(r, students, NOSD, 30)

    b = check_applying_result(result)
    print(b)





