import numpy as np
import random, pickle
import utill, student_class, apply_subject
from basic_var import SPC, NOSD, NOB, NOSJ


class Gene:
    def __init__(self, student_num):
        self.gene = np.array([i for i in range(0, NOB)])
        np.random.shuffle(self.gene)
        self.student_num = student_num  # 0번부터
        with open('students.txt', 'rb') as f:
            self.students = pickle.load(f)

    def remake_student(self):  # 유전자 바탕의 새로운 student 만들기
        new_student_subject = []
        target_student = self.students[self.student_num].return_sub()
        for i in self.gene:
            new_student_subject.append(target_student[i])
        new_student = student_class.Student(new_student_subject)
        self.students[self.student_num] = new_student

    def __repr__(self):
        return '<student: ' + str(self.student_num) + ', gene: ' + str(self.gene) + '>'


    def calculate_fitness(self):
        # 비용 문제는 나중에 수정
        apply_result = apply_subject.apply(self.students, NOSD, NOB, 50, False)
        self.fitness = NOB - len(apply_result[self.student_num].keys())
        return self.fitness


import random


class Genetic_algorithm:
    def __init__(self, student_num, population=30, mutation_chance=0.015):
        self.population = population
        self.mutation_chance = mutation_chance
        self.gene_list = []
        self.student_num = student_num

    def reset(self):
        for i in range(0, self.population):
            self.gene_list.append(Gene(self.student_num))

    def evolution(self):
        self.parents = self.select()

        self.crossed_gene = self.cross()

        self.gene_list = self.mutate()

    def select(self):
        return self.roulette_wheel()

    def roulette_wheel(self):
        # 전처리
        self.parents = []
        gene_list = self.gene_list[:]
        while True:
            gene = self.roulette_wheel_onetime(gene_list)
            self.parents.append(gene.gene)  # copy를 피하기 위해 subject 형태로 저장
            if len(self.parents) >= 2: return
            gene_list.remove(gene)

    def roulette_wheel_onetime(self, gene_list):
        fitness_list = []
        for gene in gene_list:
            gene.remake_student()
            fitness_list.append(gene.calculate_fitness())

        # 비용 => fitness 변환
        while True:
            k = 3  # 선택압
            max_var, min_var = max(fitness_list), min(fitness_list)
            a = lambda x: (max_var - x) + (max_var - min_var) / (k - 1)
            fitness_list = list(map(a, fitness_list))

            # 룰렛휠 선택
            sum_fitness = sum(fitness_list)
            before_sum = 0
            target = random.random()
            for i in range(0, len(fitness_list)):
                fitness = fitness_list[i]
                probality = before_sum + fitness / sum_fitness
                if probality < target:
                    return gene_list[i]

    def cross(self):
        return self.cycle_cross()

    def cycle_cross(self):
        for i in range(0, self.population):
            sub1, sub2 = random.sample(self.parents, 2)
            sub_list = [sub1, sub2]
            main_sub, sub_sub = sub_list[0], sub_list[1]
            gene = [-1] * 10
            while -1 in gene:
                inx_list = [i for i, value in enumerate(gene) if value == -1]
                inx = random.choice(inx_list)
                used_num = []
                while True:
                    target_num = main_sub[inx]
                    if target_num in used_num: break
                    gene[inx] = target_num
                    used_num.append(target_num)
                    inx = list(sub_sub).index(target_num)
                main_sub, sub_sub = sub_sub, main_sub
            self.gene_list[i].gene = gene

    def mutate(self):
        pass

temp = Genetic_algorithm(19)
temp.reset()
temp.roulette_wheel()
temp.cycle_cross()
