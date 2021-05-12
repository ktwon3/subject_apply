import pickle
import pick_subject
import copy

class Student:
    def __init__(self, subject):
        self.subject = subject


# subject = [[1,2,8,9,17,18,19,20,21,22], [3,10,11,22,23,17,18,19,20,24], [4,16,11,23,]]
# [[과목고유번호][블럭,남은 인원],[,]...]
'''
첫번째 시뮬에서는 과목에 대한 정보가 많이 필요하지 않아 리스트로 정리
인덱스 순서로 4A2, 4B2, 4C2, 4D2, 4F2, 4H2
인스턴스 210개를 all_student에 저장
'''

SPC = 21  # student per class, 분반당 학생수, 현재는 21로 고정
NOSD = 204 # Number Of StuDent, 총 학생수
NOB = 6  # Number Of Block, 블럭 개수
NOSJ = 25 # Number Of SubJect, 공강을 합친 과목 수

if __name__ == '__main__':
    with open("subject_block.txt", "r") as f:
        subject_block = f.read().splitlines()  # subject_block : 한 과목이 어떤 블록에 해당되는지 정리

    remain_subject, remain_block = [], [[] for i in range(NOB)]
    # remain_subject : 과목에 따른 남은 학생수, 한 딕셔너리 안에 하나의 과목, key는 분반, value는 [블럭, 남은 인원 수]
    # remain_block : 블록에 따른 남은 학생수, 블록수만큼 생성
    for i in range(len(subject_block)):
        temp = {}
        nums = subject_block[i].split()  # nums : subject_block의 각각의 숫자 분리
        for i in range(len(nums)):
            temp[i+1] = [int(nums[i]) - 1, SPC]
        remain_subject.append(temp)

    remain_subject[0] = {1: [4, NOSD], 2: [5, NOSD]}  # 공강 조정
    with open('students.txt', 'rb') as f:
        students = pickle.load(f)



    # a = students
    # for i in range(len(a)):
    #     if len(a[i].subject) != 0:
    #         print(i,a[i].subject)


    c = [0,0]



    r = copy.deepcopy(remain_subject)
    a = pick_subject.apply(r, students, NOSD, 30)

    print()
    b = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    for i in range(len(a)):
        b[len(a[i].keys())] += 1
    print(b)





