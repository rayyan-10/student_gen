import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# -----------------------------
# 1️⃣ Load Dataset
# -----------------------------
df = pd.read_csv("students.csv")

# -----------------------------
# 2️⃣ Feature & Target Split
# -----------------------------
X = df.drop(["student_id", "final_result"], axis=1)
y = df["final_result"]

# -----------------------------
# 3️⃣ Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# -----------------------------
# 4️⃣ Train Model
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# 5️⃣ Evaluate Model
# -----------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# 6️⃣ Feature Importance
# -----------------------------
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(importance)

# -----------------------------
# 7️⃣ Save Model
# -----------------------------
joblib.dump(model, "student_pass_model.pkl")
print("\nModel saved as student_pass_model.pkl")
