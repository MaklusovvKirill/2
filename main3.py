students = ["Алиса", "Боб", "Вика", "Глеб", "Дина"]
grades = [4, 3, 5, 2, 5]  

def to_score(grade):
    mapping = {2: 50, 3: 65, 4: 80, 5: 100}
    return mapping.get(grade, 0)

scores = list(map(to_score, grades))
print("Баллы:", scores)

student_scores = list(zip(students, scores))
print("Имена и баллы:", student_scores)

good_students = list(filter(lambda x: x[1] >= 70, student_scores))
print("Студенты с баллом ≥ 70:", good_students)

sorted_students = sorted(student_scores, key=lambda x: x[1], reverse=True)
print("Отсортировано по баллам (убывание):", sorted_students)

all_passed = all(score >= 50 for _, score in student_scores)
print("Все сдали?", all_passed)  # True

has_excellent = any(score >= 90 for _, score in student_scores)
print("Есть отличники?", has_excellent)  # True

sorted_by_name_len = sorted(students, key=len)
print("Имена, отсортированные по длине:", sorted_by_name_len)