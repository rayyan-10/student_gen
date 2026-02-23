import pandas as pd
from typing import List, Dict, Optional
from app.config import get_settings
from app.dataset_manager import get_dataset_manager

settings = get_settings()


def _classify_risk(pass_prob: float) -> str:
    """Classify risk level based on pass probability."""
    if pass_prob < settings.HIGH_RISK_THRESHOLD:
        return "HIGH"
    elif pass_prob < settings.LOW_RISK_THRESHOLD:
        return "MEDIUM"
    return "LOW"


def _find_weak_areas(row: pd.Series, topic_columns: List[str], threshold: int = 50) -> List[str]:
    """Find areas where the score is below threshold."""
    weak = []
    for col in topic_columns:
        if row[col] < threshold:
            # Clean up column name for display
            display_name = col.replace("_", " ").replace("topic", "").strip().title()
            weak.append(display_name)
    return weak


def predict_all_records(dataset_id: str) -> List[Dict]:
    """Run predictions for all records in a dataset."""
    manager = get_dataset_manager()
    
    model = manager.get_model(dataset_id)
    df = manager.get_dataframe(dataset_id)
    column_info = manager.get_column_info(dataset_id)
    
    feature_columns = column_info["feature_columns"]
    topic_columns = column_info["topic_columns"]
    id_column = column_info["id_column"]
    
    # Get predictions
    X = df[feature_columns]
    probabilities = model.predict_proba(X)[:, 1]
    
    results = []
    for idx, row in df.iterrows():
        prob = float(probabilities[idx])
        risk = _classify_risk(prob)
        weak = _find_weak_areas(row, topic_columns)
        
        # Build feature scores dict
        feature_scores = {}
        for col in feature_columns:
            feature_scores[col] = float(row[col])
        
        # Build topic scores dict
        topic_scores = {}
        for col in topic_columns:
            display_name = col.replace("_", " ").replace("topic", "").strip().title()
            topic_scores[display_name] = float(row[col])
        
        record = {
            "id": int(row[id_column]) if id_column else idx,
            "features": feature_scores,
            "topic_scores": topic_scores,
            "pass_probability": round(prob, 4),
            "risk_level": risk,
            "weak_areas": weak,
        }
        results.append(record)
    
    return results


def get_record_analysis(dataset_id: str, record_id: int) -> Optional[Dict]:
    """Get detailed analysis for a single record."""
    manager = get_dataset_manager()
    
    model = manager.get_model(dataset_id)
    df = manager.get_dataframe(dataset_id)
    column_info = manager.get_column_info(dataset_id)
    
    id_column = column_info["id_column"]
    feature_columns = column_info["feature_columns"]
    topic_columns = column_info["topic_columns"]
    
    # Find the record
    if id_column:
        match = df[df[id_column] == record_id]
    else:
        match = df.iloc[[record_id]] if record_id < len(df) else pd.DataFrame()
    
    if match.empty:
        return None
    
    row = match.iloc[0]
    
    # Get prediction
    X = row[feature_columns].values.reshape(1, -1)
    prob = float(model.predict_proba(X)[0][1])
    risk = _classify_risk(prob)
    weak = _find_weak_areas(row, topic_columns)
    
    # Build feature scores
    feature_scores = {}
    for col in feature_columns:
        feature_scores[col] = float(row[col])
    
    # Build topic scores
    topic_scores = {}
    for col in topic_columns:
        display_name = col.replace("_", " ").replace("topic", "").strip().title()
        topic_scores[display_name] = float(row[col])
    
    return {
        "id": int(row[id_column]) if id_column else record_id,
        "features": feature_scores,
        "topic_scores": topic_scores,
        "pass_probability": round(prob, 4),
        "risk_level": risk,
        "weak_areas": weak,
    }


def get_high_risk_records(dataset_id: str) -> List[Dict]:
    """Get all HIGH risk records from a dataset."""
    all_records = predict_all_records(dataset_id)
    return [r for r in all_records if r["risk_level"] == "HIGH"]
