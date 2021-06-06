import pickle
import copy


def set_remain_subject():
    with open("subject_block.txt", "r") as f:
        sub_block = f.read().splitlines()  # subject_block : 한 과목이 어떤 블록에 해당되는지 정리
    re_sub = []
    research_list = [i for i in range(31, 37)]
    necessary_list = [20,39]
    for i in range(len(sub_block)):
        temp = {}
        nums = sub_block[i].split()  # nums : subject_block 각각의 숫자 분리
        for j in range(len(nums)):
            if i == 0:
                temp[j + 1] = [int(nums[j]), NOSD]
            if i in research_list:
                temp[j + 1] = [int(nums[j]), 13]
            if i in necessary_list:
                temp[j + 1] = [int(nums[j]), 26]
            else:
                temp[j + 1] = [int(nums[j]), SPC]
        re_sub.append(temp)
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
            try:
                compare_dic[num] = i.split('.')[1].strip()
            except Exception:
                print(i)
                raise Exception(IndexError)

    return_dic = {}
    for s in sub_list:
        return_dic[s] = compare_dic[s]
    return return_dic


def print_remain_sub(rs):
    list_ = [i for i in range(len(rs))]
    d = label_sub(list_)
    for i in range(len(rs)):
        for j in rs[i].values():
            print(d[i], str(j[0]) + '블럭', str(j[1]) + '명')


def set_remain_block(rs, necessary_sub):
    dic = {i: [] for i in range(1, 14)}  # 13 : 총 블록 수
    rs_order = necessary_sub + [i for i in range(len(rs)) if i not in necessary_sub]
    for subject_count in rs_order:
        for class_num in rs[subject_count].keys():
            block_num, remain_student = rs[subject_count][class_num][0], rs[subject_count][class_num][1]
            dic[block_num].append({'subject': subject_count, 'class_num': class_num, 'remain_student': remain_student})

    return dic


def print_remain_block(rb):
    print('=' * 10 + 'remain_block' + '=' * 10)
    for block in rb.keys():
        print('%d블럭' % block)
        for sub_dic in rb[block]:
            temp = label_sub([sub_dic['subject']])
            subject = temp[sub_dic['subject']]
            print(subject, end='  ')
            print(str(sub_dic['class_num']) + '반  ' + str(sub_dic['remain_student']) + '명')
        print('\n')


SPC = 24  # student per class, 분반당 학생수, 현재는 24로 고정
NOSD = 204  # Number Of StuDent, 총 학생수
NOB = 10  # Number Of Block, 수강 신청을 해야하는 블럭 개수
NOSJ = 40  # Number Of SubJect, 공강을 합친 과목 수
