import joblib
import pandas as pd

model = joblib.load("student_pass_model.pkl")

new_student = {
    "attendance": 70,
    "internal_marks": 50,
    "assignment_marks": 42,
    "previous_gpa": 7.8,
    "topic_recursion": 90,
    "topic_sorting": 50,
    "topic_trees": 75,
    "topic_graphs": 28,
    "topic_dp": 62
}

df = pd.DataFrame([new_student])

prob = model.predict_proba(df)[0][1]

print("Pass Probability:", round(prob, 3))

if prob < 0.5:
    print("Risk Level: HIGH RISK")
else:
    print("Risk Level: SAFE")
