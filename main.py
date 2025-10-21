# Словарь: ключ — имя студента, значение — список кортежей (предмет, оценка)
students_grades = {
    "Алиса": [("Математика", 5), ("Физика", 4), ("Информатика", 5)],
    "Ужас": [("Математика", 3), ("Физика", 4), ("Химия", 4)],
    "Вика": [("Информатика", 5), ("Химия", 5), ("Биология", 4)],
    "Глеб": [("Математика", 2), ("Физика", 3), ("Информатика", 4)]
}

# 1. Найти все уникальные предметы (множество)
all_subjects = set()
for grades in students_grades.values():
    for subject, _ in grades:
        all_subjects.add(subject)

print("Уникальные предметы:", all_subjects)

# 2. Посчитать средний балл каждого студента
average_grades = {}
for student, grades in students_grades.items():
    total = sum(grade for _, grade in grades)
    average = total / len(grades)
    average_grades[student] = round(average, 2)

print("\nСредние баллы студентов:")
for student, avg in average_grades.items():
    print(f"{student}: {avg}")

# 3. Найти студентов с хотя бы одной пятёркой (множество имён)
students_with_fives = set()
for student, grades in students_grades.items():
    if any(grade == 5 for _, grade in grades):
        students_with_fives.add(student)

print("\nСтуденты с хотя бы одной пятёркой:", students_with_fives)