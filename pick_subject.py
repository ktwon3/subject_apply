import copy, random
import student_class, utill
from basic_var import SPC, NOSD, NOB, NOSJ

def pick_onetime(re_sub, nosj, nosd, nob, student, necessary_sub):
    students = []
    re_sub_copyed = copy.deepcopy(re_sub)  # 원인은 잘 모르겠지만 deepcopy를 해야 오류가 안 남
    remain_block = utill.set_remain_block(re_sub_copyed, necessary_sub)
    for n in range(nosd):
        track = 0  # 0 : track 미정 1 : 4단위 7블럭 2 : 2단위 3블럭
        chose_subject = []
        chose_block = []  # 블럭을 고려해줘야 구조적으로 불가능한 시간표가 나오지 않음, 다만 배정시 고려는 x
        b = [i for i in range(1, 14)]  # b는 블록 번호
        random.shuffle(b)

        for i in b:
            random.shuffle(remain_block[i])
            remain_block[i] = sort_necessary(remain_block[i], necessary_sub)

            for dic in remain_block[i]:
                if dic['subject'] in chose_subject \
                        or dic['remain_student'] <= 0 \
                        or dic['subject'] == 0 \
                        or check_condition(i, chose_block, chose_subject, track, dic['subject']): continue

                else:
                    chose_subject.append(dic['subject'])
                    chose_block.append(i)
                    dic['remain_student'] -= 1
                    track = set_track(chose_block, chose_subject, track)
                    break
            if len(chose_subject) >= nob:
                break

        if len(chose_subject) < nob - 1 \
                or len([i for i in chose_subject if i in necessary_sub]) != len(necessary_sub):
            return False, n
        elif len(chose_subject) == nob - 1:
            chose_subject.append(0)
        students.append(student(chose_subject))

    utill.print_remain_block(remain_block)
    print(remain_block)
    return True, students


def pick(re_sub, nosj, nosd, nob, student):
    # return : 학생이 듣는 과목을 Student 인스턴스로 만들어 리스트의 인덱스에 맞추어 저장
    try_count = 0
    while True:
        try_count += 1
        flag, result = pick_onetime(re_sub, nosj, nosd, nob, student, necessary_sub=[20, 39])
        if flag:
            return result, try_count
        else:
            print('%d번째 시도 : %d번째 학생 실패' %(try_count, result))


def sort_necessary(dic_list, necessary_list):  # 필수 과목이 앞쪽에 오도록 정렬
    result = []
    for dic in dic_list:
        if dic['subject'] in necessary_list:
            result.append(dic)
    others = [i for i in dic_list if i not in result]
    result += others
    return result


def confirm_pick(stu, nosj):  # 각 과목 신청자수 리스트로 반환
    result = [0] * nosj
    for s in stu:
        for j in s.subject:
            result[j] += 1
    return result


def measure_pick_time(re_sub, nosj, nosd, nob, student, n):
    sum_ = 0
    for i in range(n):
        ign, t = pick(re_sub, nosj, nosd, nob, student)
        sum_ += t
    return sum_ / n


def set_track(chose_bloc, chose_sub, track):  # 트랙 정보를 주어 공강 2블럭 가능케하기, track 넘어가면 멈추기, 과연 배제, 7-3블럭 막기
    unit_4 = [1, 2, 3, 4, 5, 6, 7, 8]
    unit_2 = [9, 10, 11, 12, 13]
    count_4 = len([i for i in chose_bloc if i in unit_4])
    count_2 = len([i for i in chose_bloc if i in unit_2])

    research_list = [i for i in range(31, 37)]
    if [i for i in chose_sub if i in research_list]: count_2 -= 1  # 과제연구는 track 2단위 고려 제외

    if count_4 == 7 and count_2 == 3 and track == 0:
        raise Exception('트랙 오류')
    elif count_2 == 3:
        track = 2
    elif count_4 == 7:
        track = 1
    else:
        track = 0
    return track


def check_condition(b, chose_b, chose_subject, track, sub):
    return check_overlap_block(b, chose_b) + check_overlab_research(sub, chose_subject) + check_track(b, track, chose_b, chose_subject)


def check_track(b, track, chose_block, chose_sub):  # 트랙에 걸리면 True, 아니면 False
    chose_b = copy.deepcopy(chose_block)
    research_list = [i for i in range(31, 37)]
    for s in chose_sub:
        if s in research_list:
            try: del(chose_b[chose_sub.index(s)])
            except:
                print(chose_b)
                print(chose_sub)
            break
    if track == 1:
        if b in [1, 2, 3, 4, 5, 6, 7, 8]: return True
    elif track == 2:
        if b in [9, 10, 11, 12, 13]: return True
    # if (10 in chose_b or 12 in chose_b) and b in [11, 13]:  # 10, 12블럭과 11, 13블럭은 트랙 문제로 인해 같이 못 들어감
    #     return True
    # if (11 in chose_b or 13 in chose_b) and b in [10,12]:
    #     return True
    if 7 in chose_b and b == 8:
        return True
    if 8 in chose_b and b == 7:
        return True
    return False


def check_overlab_research(sub, chose_subject): # 과제연구가 있을시 True, 과제연구 중복 고려
    research_list = [i for i in range(31, 37)]
    if sub in research_list:
        if [i for i in chose_subject if i in research_list]:
            return True
    return False


def check_overlap_block(b, chose_b):
    if b == 7:
        if 10 in chose_b or 12 in chose_b: return True
    elif (b == 10 or b == 12) and 7 in chose_b: return True
    elif b == 8:
        if 11 in chose_b or 13 in chose_b: return True
    elif (b == 11 or b == 13) and 8 in chose_b: return True
    return False





if __name__ == '__main__':
    SPC = utill.SPC   # student per class, 분반당 학생수, 현재는 21로 고정
    NOSD = utill.NOSD  # Number Of StuDent, 총 학생수
    NOB = utill.NOB  # Number Of Block, 블럭 개수
    NOSJ = utill.NOSJ  # Number Of SubJect, 공강을 합친 과목 수

    remain_subject = utill.set_remain_subject()

    sum_count = 0
    r = copy.deepcopy(remain_subject)
    temp, _ = pick(r, NOSJ, NOSD, NOB, student_class.Student)
    if input('저장하시겠습니까? (Y/N)') == 'Y':
        utill.save_file('students.txt', temp)

    for i in temp:
        print(i.subject)
        # print(utill.label_sub(i.return_sub()))
