import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, Union

class PlayoffPredictor:
    """Predict NBA playoff return time for teams"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize the predictor
        
        Args:
            model_path: Path to directory containing model files
        """
        if model_path is None:
            # Default to data/models directory
            model_path = Path(__file__).parent / "data" / "models"
        else:
            model_path = Path(model_path)
        
        self.model = joblib.load(model_path / "playoff_return_model.pkl")
        self.scaler = joblib.load(model_path / "feature_scaler.pkl")
        self.feature_cols = joblib.load(model_path / "feature_columns.pkl")
    
    def predict(self, team_data: Union[Dict, pd.DataFrame]) -> float:
        """
        Predict years to playoff return
        
        Args:
            team_data: Dictionary or DataFrame with team features
            
        Returns:
            Predicted years to playoff return
        """
        if isinstance(team_data, dict):
            team_data = pd.DataFrame([team_data])
        
        # Ensure all required features are present
        missing_features = set(self.feature_cols) - set(team_data.columns)
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        # Select and order features
        X = team_data[self.feature_cols]
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction = self.model.predict(X_scaled)[0]
        
        return prediction
    
    def predict_batch(self, teams_data: pd.DataFrame) -> np.ndarray:
        """
        Predict for multiple teams
        
        Args:
            teams_data: DataFrame with multiple teams' features
            
        Returns:
            Array of predictions
        """
        X = teams_data[self.feature_cols]
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance from the model"""
        if hasattr(self.model, 'feature_importances_'):
            return pd.DataFrame({
                'feature': self.feature_cols,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        return None