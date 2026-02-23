import os
import json
import pandas as pd
import joblib
from pathlib import Path
from typing import Optional, Dict, List
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from app.config import get_settings

settings = get_settings()


class DatasetManager:
    """Manages multiple datasets and their trained models."""
    
    def __init__(self):
        self.datasets: Dict[str, Dict] = {}
        self.models: Dict[str, any] = {}
        self._ensure_directories()
        self._load_metadata()
    
    def _ensure_directories(self):
        """Create upload and models directories if they don't exist."""
        Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
        Path(settings.MODELS_DIR).mkdir(exist_ok=True)
    
    def _load_metadata(self):
        """Load existing datasets metadata from disk."""
        metadata_path = Path(settings.UPLOAD_DIR) / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                self.datasets = json.load(f)
    
    def _save_metadata(self):
        """Save datasets metadata to disk."""
        metadata_path = Path(settings.UPLOAD_DIR) / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(self.datasets, f, indent=2)
    
    def _detect_columns(self, df: pd.DataFrame) -> Dict[str, any]:
        """Auto-detect column types in the dataset."""
        columns = df.columns.tolist()
        
        # Detect ID column (usually first column or contains 'id')
        id_column = None
        for col in columns:
            if 'id' in col.lower() or col == columns[0]:
                id_column = col
                break
        
        # Detect target column (binary, usually last or contains 'result', 'pass', 'fail', 'target')
        target_column = None
        target_keywords = ['result', 'pass', 'fail', 'target', 'outcome', 'status', 'label']
        
        for col in reversed(columns):
            if col == id_column:
                continue
            # Check if binary
            unique_vals = df[col].nunique()
            if unique_vals == 2:
                target_column = col
                break
        
        # If not found by keywords, use last column if binary
        if target_column is None:
            last_col = columns[-1]
            if last_col != id_column and df[last_col].nunique() == 2:
                target_column = last_col
        
        # Feature columns are everything except ID and target
        feature_columns = [col for col in columns if col != id_column and col != target_column]
        
        # Detect numeric topic/score columns (for weak area analysis)
        topic_columns = []
        for col in feature_columns:
            if df[col].dtype in ['int64', 'float64']:
                # Check if it looks like a score (0-100 range or similar)
                col_max = df[col].max()
                col_min = df[col].min()
                if col_min >= 0 and col_max <= 100:
                    topic_columns.append(col)
        
        return {
            "id_column": id_column,
            "target_column": target_column,
            "feature_columns": feature_columns,
            "topic_columns": topic_columns,
            "all_columns": columns
        }
    
    def upload_dataset(self, file_path: str, dataset_id: str) -> Dict:
        """Upload and process a new dataset."""
        # Load CSV
        df = pd.read_csv(file_path)
        
        # Detect columns
        column_info = self._detect_columns(df)
        
        if column_info["target_column"] is None:
            raise ValueError("Could not detect a binary target column. Please ensure your CSV has a binary outcome column.")
        
        # Save dataset
        dataset_path = Path(settings.UPLOAD_DIR) / f"{dataset_id}.csv"
        df.to_csv(dataset_path, index=False)
        
        # Train model
        model_info = self._train_model(df, column_info, dataset_id)
        
        # Store metadata
        self.datasets[dataset_id] = {
            "dataset_path": str(dataset_path),
            "column_info": column_info,
            "model_info": model_info,
            "row_count": len(df),
            "created_at": pd.Timestamp.now().isoformat()
        }
        
        self._save_metadata()
        
        return {
            "dataset_id": dataset_id,
            "rows": len(df),
            "columns": column_info,
            "model_accuracy": model_info["accuracy"]
        }
    
    def _train_model(self, df: pd.DataFrame, column_info: Dict, dataset_id: str) -> Dict:
        """Train a RandomForest model for the dataset."""
        # Prepare features and target
        X = df[column_info["feature_columns"]]
        y = df[column_info["target_column"]]
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42
        )
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=5,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Save model
        model_path = Path(settings.MODELS_DIR) / f"{dataset_id}.pkl"
        joblib.dump(model, model_path)
        
        # Cache model in memory
        self.models[dataset_id] = model
        
        return {
            "model_path": str(model_path),
            "accuracy": round(accuracy, 4),
            "n_features": len(column_info["feature_columns"])
        }
    
    def get_model(self, dataset_id: str):
        """Get the trained model for a dataset."""
        if dataset_id not in self.models:
            if dataset_id not in self.datasets:
                raise ValueError(f"Dataset '{dataset_id}' not found")
            
            model_path = self.datasets[dataset_id]["model_info"]["model_path"]
            self.models[dataset_id] = joblib.load(model_path)
        
        return self.models[dataset_id]
    
    def get_dataframe(self, dataset_id: str) -> pd.DataFrame:
        """Get the dataframe for a dataset."""
        if dataset_id not in self.datasets:
            raise ValueError(f"Dataset '{dataset_id}' not found")
        
        dataset_path = self.datasets[dataset_id]["dataset_path"]
        return pd.read_csv(dataset_path)
    
    def get_column_info(self, dataset_id: str) -> Dict:
        """Get column information for a dataset."""
        if dataset_id not in self.datasets:
            raise ValueError(f"Dataset '{dataset_id}' not found")
        
        return self.datasets[dataset_id]["column_info"]
    
    def list_datasets(self) -> List[Dict]:
        """List all available datasets."""
        return [
            {
                "dataset_id": dataset_id,
                "rows": info["row_count"],
                "columns": len(info["column_info"]["all_columns"]),
                "accuracy": info["model_info"]["accuracy"],
                "created_at": info["created_at"]
            }
            for dataset_id, info in self.datasets.items()
        ]
    
    def delete_dataset(self, dataset_id: str):
        """Delete a dataset and its model."""
        if dataset_id not in self.datasets:
            raise ValueError(f"Dataset '{dataset_id}' not found")
        
        # Delete files
        dataset_path = Path(self.datasets[dataset_id]["dataset_path"])
        model_path = Path(self.datasets[dataset_id]["model_info"]["model_path"])
        
        if dataset_path.exists():
            dataset_path.unlink()
        if model_path.exists():
            model_path.unlink()
        
        # Remove from memory
        del self.datasets[dataset_id]
        if dataset_id in self.models:
            del self.models[dataset_id]
        
        self._save_metadata()


# Global instance
_manager = None


def get_dataset_manager() -> DatasetManager:
    """Get the global DatasetManager instance."""
    global _manager
    if _manager is None:
        _manager = DatasetManager()
    return _manager
