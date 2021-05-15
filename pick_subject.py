import copy, random
import student_class, utill


def pick(re_sub, nosj, nosd, nob, student):
    # return : 학생이 듣는 과목을 Student 인스턴스로 만들어 리스트의 인덱스에 맞추어 저장
    try_count = 0
    rs_ = [0] * len(re_sub)
    for i in range(len(re_sub)):
        a = list(re_sub[i].values())
        for j in a:
            rs_[i] += j[1]  # rs_는 과목당 듣는 학생수, (분반) * (분반당 학생수)의 총합
    while True:
        try_count += 1
        flag = True
        students = []
        rs = copy.deepcopy(rs_)  # rs는 과목 배정을 위한 것, deepcopy는 변수간 영향 x
        re_sub_copyed = copy.deepcopy(re_sub)
        for n in range(nosd):
            chose_subject = []
            chose_block = []  # 블럭을 고려해줘야 구조적으로 불가능한 시간표가 나오지 않음, 다만 배정시 고려는 x
            s = [i for i in range(1, nosj)]  # s는 과목 번호
            random.shuffle(s)
            for i in s:
                if rs[i] <= 0:
                    continue
                else:
                    for j in re_sub_copyed[i].keys():
                        if re_sub_copyed[i][j][0] in chose_block or re_sub_copyed[i][j][1] <= 0: continue
                        else:
                            chose_subject.append(i)
                            chose_block.append(re_sub_copyed[i][j][0])
                            chose_block = utill.add_overlap_block(re_sub_copyed[i][j][0], chose_block)
                            rs[i] -= 1
                            re_sub_copyed[i][j][1] -= 1
                            break
                if len(chose_subject) >= nob:
                    break

            if len(chose_subject) < nob - 1:
                # if n >= 200:
                #     print(str(try_count) + '번째 시도: ' + str(n) + '번째 학생 실패')
                #    print(rs)
                #     print(chose_block)
                #     print(len(chose_subject))
                #     print('=' * 100)
                flag = False
                # return n
                break
            elif len(chose_subject) == nob - 1:
                chose_subject.append(0)
            students.append(student(chose_subject))
            if not flag:
                break
        if flag:
            break
    return students, try_count


def check_pick(stu, nosj):  # 각 과목 신청자수 리스트로 반환
    result = [0] * nosj
    for s in stu:
        for j in s.subject:
            result[j] += 1
    return result


def check_pick_time(re_sub, nosj, nosd, nob, student, n):
    avr = 0
    for i in range(n):
        ign, t = pick(re_sub, nosj, nosd, nob, student)
        avr += t
    return avr / n


def limit_track(r_b):
    unit_4 = [1, 2, 3, 4, 5, 6, 7, 8]
    unit_2 = [9, 10, 11, 12, 13]
    count_4, count_2 = 0, 0
    result = set(r_b)
    for i in r_b:
        if i in unit_4:
            count_4 += 1
        if i in unit_2:
            count_2 += 1
        if count_4 == 7:
            result.union(set(unit_4))
        if count_2 == 3:
            result.union(set(unit_2))
    return list(result)


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

    print(check_pick(temp, NOSJ))
