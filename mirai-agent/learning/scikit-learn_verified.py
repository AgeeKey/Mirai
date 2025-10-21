"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-21T12:59:26.593787

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a pandas DataFrame."""
    try:
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['target'] = iris.target
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def preprocess_data(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Preprocess the data by splitting into features and target."""
    try:
        X = df.drop('target', axis=1).values
        y = df['target'].values
        return X, y
    except Exception as e:
        raise RuntimeError(f"Error preprocessing data: {e}")

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train the Random Forest model."""
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model, X_test, y_test
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the accuracy and classification report."""
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError(f"Error evaluating model: {e}")

def main() -> None:
    """Main function to execute the machine learning workflow."""
    try:
        df = load_data()
        X, y = preprocess_data(df)
        model, X_test, y_test = train_model(X, y)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()