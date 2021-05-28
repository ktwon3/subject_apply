import pickle
import copy


def set_remain_subject():
    with open("subject_block.txt", "r") as f:
        sub_block = f.read().splitlines()  # subject_block : 한 과목이 어떤 블록에 해당되는지 정리
    re_sub = []

    for i in range(len(sub_block)):
        temp = {}
        nums = sub_block[i].split()  # nums : subject_block의 각각의 숫자 분리
        for j in range(len(nums)):
            if i == 0:
                temp[j + 1] = [int(nums[j]), NOSD]
            else:
                temp[j + 1] = [int(nums[j]), SPC]
        re_sub.append(temp)

    #  re_sub[0] = {5: [4, 200], 6: [5, 400]}  # 공강 조정, 어떻게 조정해야 할지 더 찾아봐야 함
    return re_sub


def save_file(file_name, data):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def add_overlap_block(b, cb):
    chose_b = copy.deepcopy(cb)
    if b == 7:
        if 10 not in chose_b: chose_b.append(10)
        if 12 not in chose_b: chose_b.append(12)
    elif (b == 10 or b == 12) and 7 not in chose_b:
        chose_b.append(7)
    elif b == 8:
        if 11 not in chose_b: chose_b.append(11)
        if 13 not in chose_b: chose_b.append(13)
    elif (b == 11 or b == 13) and 8 not in chose_b:
        chose_b.append(8)
    return chose_b


def label_sub(sub_list):
    compare_dic = {}

    with open('sub__name.txt', 'r', encoding='UTF8') as f:
        raw = f.read().splitlines()

    for s in raw:
        for i in s.split('\t'):
            num = int(i.split('.')[0])
            try : compare_dic[num] = i.split('.')[1].strip()
            except:
                print(i)
                raise Exception(IndexError)

    return_dic = {}
    for s in sub_list:
        return_dic[s] = compare_dic[s]
    return return_dic



SPC = 24  # student per class, 분반당 학생수, 현재는 24로 고정
NOSD = 204  # Number Of StuDent, 총 학생수
NOB = 10  # Number Of Block, 수강 신청을 해야하는 블럭 개수
NOSJ = 40  # Number Of SubJect, 공강을 합친 과목 수
