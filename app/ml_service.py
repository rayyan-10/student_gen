import joblib
import pandas as pd
from app.config import get_settings

settings = get_settings()

TOPIC_COLUMNS = [
    "topic_recursion",
    "topic_sorting",
    "topic_trees",
    "topic_graphs",
    "topic_dp",
]

FEATURE_COLUMNS = [
    "attendance",
    "internal_marks",
    "assignment_marks",
    "previous_gpa",
] + TOPIC_COLUMNS


# ── Model & Data Loading ──────────────────────────────────────────────

_model = None
_students_df = None


def load_model():
    """Load the trained RandomForest model from disk."""
    global _model
    _model = joblib.load(settings.MODEL_PATH)
    return _model


def get_model():
    """Return the loaded model (lazy load if needed)."""
    global _model
    if _model is None:
        load_model()
    return _model


def load_students() -> pd.DataFrame:
    """Load students.csv and cache it."""
    global _students_df
    _students_df = pd.read_csv(settings.DATA_PATH)
    return _students_df


def get_students() -> pd.DataFrame:
    """Return the cached student dataframe (lazy load if needed)."""
    global _students_df
    if _students_df is None:
        load_students()
    return _students_df.copy()


# ── Risk Classification ───────────────────────────────────────────────

def _classify_risk(pass_prob: float) -> str:
    if pass_prob < settings.HIGH_RISK_THRESHOLD:
        return "HIGH"
    elif pass_prob < settings.LOW_RISK_THRESHOLD:
        return "MEDIUM"
    return "LOW"


def _find_weak_topics(row: pd.Series, threshold: int = 50) -> list[str]:
    """Return topic names where the student scored below the threshold."""
    weak = []
    for col in TOPIC_COLUMNS:
        if row[col] < threshold:
            weak.append(col.replace("topic_", "").title())
    return weak


# ── Analysis Functions ─────────────────────────────────────────────────

def predict_all_students() -> list[dict]:
    """Run predictions for every student and return enriched records."""
    model = get_model()
    df = get_students()

    X = df[FEATURE_COLUMNS]
    probabilities = model.predict_proba(X)[:, 1]

    results = []
    for idx, row in df.iterrows():
        prob = float(probabilities[idx])
        risk = _classify_risk(prob)
        weak = _find_weak_topics(row)
        topic_scores = {
            col.replace("topic_", "").title(): float(row[col])
            for col in TOPIC_COLUMNS
        }
        results.append({
            "student_id": int(row["student_id"]),
            "attendance": float(row["attendance"]),
            "internal_marks": float(row["internal_marks"]),
            "assignment_marks": float(row["assignment_marks"]),
            "previous_gpa": float(row["previous_gpa"]),
            "topic_scores": topic_scores,
            "pass_probability": round(prob, 4),
            "risk_level": risk,
            "weak_topics": weak,
        })
    return results


def get_student_analysis(student_id: int) -> dict | None:
    """Return a detailed analysis dict for one student, or None."""
    model = get_model()
    df = get_students()

    match = df[df["student_id"] == student_id]
    if match.empty:
        return None

    row = match.iloc[0]
    X = row[FEATURE_COLUMNS].values.reshape(1, -1)
    prob = float(model.predict_proba(X)[0][1])
    risk = _classify_risk(prob)
    weak = _find_weak_topics(row)
    topic_scores = {
        col.replace("topic_", "").title(): float(row[col])
        for col in TOPIC_COLUMNS
    }

    return {
        "student_id": int(row["student_id"]),
        "attendance": float(row["attendance"]),
        "internal_marks": float(row["internal_marks"]),
        "assignment_marks": float(row["assignment_marks"]),
        "previous_gpa": float(row["previous_gpa"]),
        "topic_scores": topic_scores,
        "pass_probability": round(prob, 4),
        "risk_level": risk,
        "weak_topics": weak,
    }


def get_high_risk_students() -> list[dict]:
    """Return only students classified as HIGH risk."""
    return [s for s in predict_all_students() if s["risk_level"] == "HIGH"]
