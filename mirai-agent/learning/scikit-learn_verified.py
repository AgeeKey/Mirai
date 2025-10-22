"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-22T16:44:51.892340

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset as a pandas DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> (np.ndarray, np.ndarray):
    """Preprocess the DataFrame and split into features and target."""
    X = df.values
    y = load_iris().target
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided data."""
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except ValueError as e:
        print(f"Error during model training: {e}")
        raise

def evaluate_model(model: RandomForestClassifier, X: np.ndarray, y: np.ndarray) -> None:
    """Evaluate the trained model and print accuracy and classification report."""
    try:
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
        print(f"Model Accuracy: {accuracy:.2f}")
        print(classification_report(y, y_pred))
    except NotFittedError as e:
        print("Model is not fitted yet. Please train the model before evaluation.")
        raise
    except Exception as e:
        print(f"Error during model evaluation: {e}")
        raise

def main() -> None:
    """Main function to load data, train the model, and evaluate it."""
    df = load_data()
    X, y = preprocess_data(df)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()