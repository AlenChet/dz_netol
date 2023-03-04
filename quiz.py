# списки лекторов и студентов в глобал
lecturer_list = []
students_list = []


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        students_list.append(self)

    def add_course(self, course_name):
        self.finished_courses.append(course_name)

    def grade_lec(self, lecturer, course, grade_lec):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.course_list \
                and grade_lec <= 10:
            if course in lecturer.grades_lec:
                lecturer.grades_lec[course] += [grade_lec]
            else:
                lecturer.grades_lec[course] = [grade_lec]
        else:
            return "Ошибка"

    def calculate_average(self):
        all_grades_student = []
        if not self.grades.values():
            return f"У студента:{self.name} пока нет оценок"
        else:
            for evals in self.grades.values():
                for eval in evals:
                    all_grades_student.append(eval)
            return round(sum(all_grades_student) / len(all_grades_student), 1)

    def __gt__(self, other):
        if self.calculate_average() == f"У студента:{self.name} нет оценок" or \
                other.calculate_average() == f"У студента:{self.name} нет оценок":
            return 'Невозможно сравнить'
        else:
            return self.calculate_average() > other.calculate_average()

    def __str__(self):
        return f"""
        Имя: {self.name}
        Фамилия: {self.surname}
        Средняя оценка за домашнее задание: {self.calculate_average()}
        Курсы в процессе изучения: {''.join(self.courses_in_progress)}
        Завершенные курсы: {''.join(self.finished_courses)}
        """


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.course_list = []

    def __str__(self):
        return f"""
           Имя: {self.name}
           Фамилия: {self.surname}
           """

class Reviewer(Mentor):
    def evals_stud(self, student, course, grade):
        if isinstance(student, Student) and course in self.course_list and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return "Ошибка"

    def __str__(self):
        return f"{super().__str__()}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades_lec = {}
        lecturer_list.append(self)

    def average_grades_lec(self):
        all_grades_lec = []
        if not self.grades_lec.values():
            return f"У лектора: {self.name} нет оценок"
        else:
            for evals in self.grades_lec.values():
                for eval in evals:
                    all_grades_lec.append(eval)
            return round(sum(all_grades_lec) / len(all_grades_lec), 1)

    def __gt__(self, other):
        if self.average_grades_lec() == f"У лектора: {self.name} нет оценок" or other.average_grades_lec() == f"У лектора: {self.name} нет оценок":
            return "Сравнить невозможно"
        else:
            return self.average_grades_lec() > other.average_grades_lec()

    def __str__(self):
        return f"{super().__str__()}Средняя оценка за лекции: {self.average_grades_lec()}"

    def average_lec(self, course):
        if not course in self.course_list:
            return f"Лектор: {self.name} не проводит лекции по курсу: {course}"
        elif not self.grades_lec.get(course):
            return f"У лектора: {self.name} по курсу {course} еще нет оценок"
        else:
            return f"Cредняя оценка лектора: {self.name} за курс {course}: " \
                   f"{round(sum(self.grades_lec[course]) / len(self.grades_lec[course]), 1)}"


def get_course_lec(lecturer_list, course):
    grades_list_lec = []
    for lecturer in lecturer_list:
        if not course in lecturer.course_list:
            print(f"Преподаватель: {lecturer.name} не ведет лекции по курсу: {course}")
        elif not course in lecturer.grades_lec:
            print(f"У преподавателя: {lecturer.name} нет оценок за курс: {course}")
        else:
            for mark in lecturer.grades_lec[course]:
                grades_list_lec.append(mark)
    if len(grades_list_lec) == 0:
        return "Ошибка, у преподавателей нет оценок!"
    else:
        return f"Средняя оценка всех лекторов за лекции в рамках курса {course}: " \
               f"{round(sum(grades_list_lec) / len(grades_list_lec), 1)}"

def get_course_stud(students_list, course):
    grades_list_stud = []
    for student in students_list:
        if not course in student.courses_in_progress:
            print(f"Студент: {student.name} не изучает курс {course}")
        elif not course in student.grades:
            print(f"У студентa: {student.name} нет оценок за курс: {course}")
        else:
            for mark in student.grades[course]:
                grades_list_stud.append(mark)
    if len(grades_list_stud) == 0:
        return 'Ошибка у студентов нет оценок!'
    else:
        return f'Средняя оценка всех студентов за лекции в рамках курса {course}: ' \
               f'{round(sum(grades_list_stud) / len(grades_list_stud), 1)}'

student_one = Student("Алёна", "Чет", "женский")
student_one.add_course("git")
student_one.courses_in_progress += ["python"]

student_two = Student("Иван", "Иванов", "мужской")
student_two.add_course("python")
student_two.courses_in_progress += ["git"]

reviewer_one = Reviewer("Олег", "Булыгин")
reviewer_one.course_list += ["python"]

reviewer_two = Reviewer("Дмитрий", "Качалов")
reviewer_two.course_list += ["git"]

lecturer_one = Lecturer("Александр", "Бардин")
lecturer_one.course_list += ["python"]

lecturer_two = Lecturer("Евгений", "Шмаргунов")
lecturer_two.course_list += ["git"]

reviewer_one.evals_stud(student_one, "python", 10)
reviewer_two.evals_stud(student_two, "git", 5)
reviewer_one.evals_stud(student_one, "python", 10)
reviewer_two.evals_stud(student_two, "git", 7)


student_one.grade_lec(lecturer_one, "python", 10)
student_two.grade_lec(lecturer_one, "python", 7)
student_two.grade_lec(lecturer_two, "git", 8)
student_one.grade_lec(lecturer_two, "git", 8)



print(f"Студент 1: {student_one}")
print(f"Студент 2: {student_two}")

print(f"Ревьюер 1: {reviewer_one}")
print(f"Ревьюер 2: {reviewer_two}")

print(f"Лектор 1: {lecturer_one}")
print(f"Лектор 2: {lecturer_two}")

print(student_one < student_two)
print(student_one > student_two)
print(student_one == student_two)
print(student_one != student_two)

print(lecturer_one < lecturer_two)
print(lecturer_one > lecturer_two)
print(lecturer_one == lecturer_two)
print(lecturer_one != lecturer_two)

print(lecturer_one.average_grades_lec())
print(lecturer_two.average_grades_lec())
print(lecturer_one.average_lec("python"))
print(lecturer_two.average_lec("git"))
print(lecturer_one.average_lec("git"))
print(lecturer_two.average_lec("python"))

print(get_course_stud(students_list, "git"))
print(get_course_stud(students_list, "python"))
print(get_course_lec(lecturer_list, "git"))
print(get_course_lec(lecturer_list, "python"))
