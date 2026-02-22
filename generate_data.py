import pandas as pd
import random

data = []

for student_id in range(1, 301):  # 300 students

    attendance = random.randint(50, 100)
    internal_marks = random.randint(30, 95)
    assignment_marks = random.randint(30, 95)
    previous_gpa = round(random.uniform(4.5, 9.5), 2)

    topic_recursion = random.randint(25, 95)
    topic_sorting = random.randint(25, 95)
    topic_trees = random.randint(25, 95)
    topic_graphs = random.randint(25, 95)
    topic_dp = random.randint(25, 95)

    # Simple rule to simulate realistic pass/fail
    avg_score = (
        internal_marks +
        assignment_marks +
        topic_recursion +
        topic_sorting +
        topic_trees +
        topic_graphs +
        topic_dp
    ) / 7

    if avg_score > 55 and attendance > 60 and previous_gpa > 5.5:
        final_result = 1
    else:
        final_result = 0

    data.append([
        student_id,
        attendance,
        internal_marks,
        assignment_marks,
        previous_gpa,
        topic_recursion,
        topic_sorting,
        topic_trees,
        topic_graphs,
        topic_dp,
        final_result
    ])

columns = [
    "student_id",
    "attendance",
    "internal_marks",
    "assignment_marks",
    "previous_gpa",
    "topic_recursion",
    "topic_sorting",
    "topic_trees",
    "topic_graphs",
    "topic_dp",
    "final_result"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("students.csv", index=False)

print("Generated 300 student records successfully.")
