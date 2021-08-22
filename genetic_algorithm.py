import numpy as np
import random, pickle
import utill, student_class, apply_subject
from basic_var import SPC, NOSD, NOB, NOSJ

class Chromosome:
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

	def return_studnets(self):
		return self.students

	def calculate_fitness(self):
		apply_result = apply_subject.apply(self.students, NOSD, NOB, 50, False)
		self.fitenss = len(apply_result[self.student_num].keys())
		print(apply_result)




def create_chromosome_list():
	chromosome_list = []



if __name__ == "__main__":
	temp = np.array([i for i in range(0, NOB)])

	c = Chromosome(1)
	c.remake_student()
	c.calculate_fitness()



