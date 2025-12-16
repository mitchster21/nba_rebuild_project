import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

def calculate_years_to_playoffs(df):
    """
    For teams that made playoffs then missed, calculate how many years until they return
    """
    df = df.sort_values(['team_name', 'season'])
    df['prev_playoffs'] = df.groupby('team_name')['playoffs'].shift(1)
    df['years_to_return'] = np.nan
    
    results = []
    for team in df['team_name'].unique():
        team_data = df[df['team_name'] == team].reset_index(drop=True)
        
        for i in range(len(team_data)):
            # Check if team made playoffs last year but missed this year
            if i > 0 and team_data.loc[i-1, 'playoffs'] == 1 and team_data.loc[i, 'playoffs'] == 0:
                # Count years until next playoff appearance
                years = 0
                found_playoff = False
                for j in range(i+1, len(team_data)):
                    years += 1
                    if team_data.loc[j, 'playoffs'] == 1:
                        found_playoff = True
                        break
                
                # Only include if they eventually made playoffs (not still waiting)
                if found_playoff:
                    row = team_data.loc[i].copy()
                    row['years_to_return'] = years
                    results.append(row)
    
    return pd.DataFrame(results)

def train_and_save_model():
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # Load the data
    data_path = project_root / 'src' / 'nba_rebuilds' / 'data' / 'final_combined_file.csv'
    df = pd.read_csv(data_path)
    
    # Create training dataset
    train_df = calculate_years_to_playoffs(df)
    
    print(f"Training samples: {len(train_df)}")
    print(f"Years to return - Min: {train_df['years_to_return'].min()}, Max: {train_df['years_to_return'].max()}, Mean: {train_df['years_to_return'].mean():.2f}")
    
    # Select features for prediction
    feature_cols = [
        'roster_size', 'retained_players', 'new_players', 'departed_players',
        'continuity_pct', 'avg_age', 'median_age', 'oldest_player', 'youngest_player',
        'avg_experience', 'rookies_count', 'all_nba_count'
    ]
    
    X = train_df[feature_cols]
    y = train_df['years_to_return']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train multiple models and compare
    models = {
        'Random Forest': RandomForestRegressor(n_estimators=200, max_depth=10, min_samples_split=5, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42)
    }
    
    best_model = None
    best_score = float('inf')
    results = {}
    
    for name, model in models.items():
        # Train
        model.fit(X_train_scaled, y_train)
        
        # Predict
        y_pred = model.predict(X_test_scaled)
        
        # Evaluate
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='neg_mean_absolute_error')
        cv_mae = -cv_scores.mean()
        
        results[name] = {
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2,
            'CV_MAE': cv_mae
        }
        
        print(f"\n{name}:")
        print(f"  MAE: {mae:.2f} years")
        print(f"  RMSE: {rmse:.2f} years")
        print(f"  R² Score: {r2:.3f}")
        print(f"  Cross-Val MAE: {cv_mae:.2f} years")
        
        if mae < best_score:
            best_score = mae
            best_model = model
    
    print(f"\n\nBest Model: {[k for k, v in results.items() if v['MAE'] == best_score][0]}")
    
    # Feature importance
    if hasattr(best_model, 'feature_importances_'):
        importance_df = pd.DataFrame({
            'feature': feature_cols,
            'importance': best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(importance_df.to_string(index=False))
    
    # Create models directory in data folder
    models_dir = project_root / 'src' / 'nba_rebuilds' / 'data' / 'models'
    models_dir.mkdir(exist_ok=True)
    
    # Save the model and scaler
    joblib.dump(best_model, models_dir / 'playoff_return_model.pkl')
    joblib.dump(scaler, models_dir / 'feature_scaler.pkl')
    joblib.dump(feature_cols, models_dir / 'feature_columns.pkl')
    
    print(f"\n✓ Model saved to {models_dir}/")
    print("✓ Files created:")
    print("  - playoff_return_model.pkl")
    print("  - feature_scaler.pkl")
    print("  - feature_columns.pkl")
    
    return best_model, scaler, feature_cols

if __name__ == "__main__":
    train_and_save_model()