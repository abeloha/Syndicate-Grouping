import operator
from itertools import groupby


class Student:
    def __init__(self, name, grade, gender, specialisation, foreigner="Nigerian"):
        self.name = name
        self.grade = grade
        self.gender = gender
        self.foreigner = foreigner
        self.specialisation = specialisation

    def __repr__(self):
        return repr((self.grade, self.gender, self.foreigner, self.specialisation, self.name))


students = [
    Student("sam", "C+", "male", "Nurse", "Nigerian"),
    Student("David", "1", "male", "Eng", "Gana"),
    Student("Tunde", "1", "female", "Nurse", "Nigerian"),
    Student("Ayomide", "1", "male", "med(surg)", "Chad"),
    Student("Tutu", "2", "male", "med(lab)", "Nigerian"),
    Student("Tope", "C+", "female", "med(surg)", "Nigerian"),
    Student("Daudu", "3", "male", "med(surg)", "Nigerian"),
    Student("Tonto", "C+", "male", "Eng", "Nigerian"),
    Student("Mariam", "2", "male", "Law", "Kotonu"),
    Student("Sunday", "3", "male", "med(lab)", "Nigerian"),
    Student("Mary", "2", "female", "med(lab)", "Nigerian"),
    Student("Ayo", "3", "male", "Eng", "Togo"),
    Student("Wahid", "C+", "female", "med(surg)", "Nigerian"),
    Student("Saburu", "3", "male", "med(surg)", "Nigerian"),
    Student("Tayo", "C+", "male", "Eng", "Nigerian"),
    Student("Muyiwa", "2", "male", "Law", "Nigerian"),
    Student("Ope", "3", "male", "med(lab)", "Nigerian"),
    Student("Tina", "2", "female", "med(lab)", "Libya"),
    Student("Tomiwa", "3", "male", "Eng", "Nigerian"),
    Student("Saburu", "3", "male", "med(surg)", "Nigerian"),
    Student("Tayo", "C+", "male", "Eng", "Nigerian"),
    Student("Muyiwa", "2", "male", "Law", "Nigerian"),
    Student("Ope", "3", "male", "med(lab)", "Nigerian"),
    Student("Tina", "2", "female", "med(lab)", "Libya"),
    Student("Tomiwa", "3", "male", "Eng", "Nigerian"),

]

NUMBER_OF_GROUPS = 5
groups = [[] for i in range(NUMBER_OF_GROUPS)]
counter = 0

reverse = False


def reverse_sort():
    global reverse
    reverse = not reverse
    return reverse


gender_attr = operator.attrgetter("gender")
grade_attr = operator.attrgetter("grade")
natinal_attr = operator.attrgetter("foreigner")
spe_attr = operator.attrgetter("specialisation")


grouped_students = []
# Group by national
for national_key, national_vals in groupby(sorted(students, key=grade_attr), gender_attr):
    grouped_students.append(
        [
            [
                list(grade_vals)
                # Group by grade
                for grade_key, grade_vals in groupby(sorted(gender_vals, key=natinal_attr), natinal_attr)
            ]
            # Group by gender
            for gender_key, gender_vals in groupby(sorted(national_vals, key=gender_attr), grade_attr)
        ]
    )

for gender_group in grouped_students:
    for national_group in gender_group:
        for specialisation_group in national_group:
            for student in sorted(specialisation_group, key=spe_attr, reverse=reverse_sort()):
                groups[counter].append(student)
                counter = (counter + 1) % NUMBER_OF_GROUPS


def print_group(student_groups):
    for i in range(len(student_groups)):
        print("Group {0}:".format(i + 1))
        for member in student_groups[i]:
            print(member)


print_group(groups)
