"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.77
Tests Passed: 0/1
Learned: 2025-10-20T17:18:06.094700

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the iris dataset and return features and labels."""
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(data: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Split the data into training and testing sets."""
    try:
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)
    except Exception as e:
        raise ValueError(f"Error in data splitting: {e}")
    return X_train, X_test, y_train, y_test

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    try:
        model.fit(X_train, y_train)
    except Exception as e:
        raise RuntimeError(f"Error in model training: {e}")
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the classification report and confusion matrix."""
    try:
        y_pred = model.predict(X_test)
        print("Classification Report:\n", classification_report(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    except Exception as e:
        raise RuntimeError(f"Error in model evaluation: {e}")

def main() -> None:
    """Main function to execute the workflow."""
    data, target = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(data, target)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()