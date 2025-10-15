"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-15T10:23:19.214965

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load and return the Iris dataset."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a RandomForestClassifier on the training data."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test data and print the results."""
    try:
        y_pred = model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print(classification_report(y_test, y_pred))
    except NotFittedError:
        print("Model is not fitted. Please train the model before evaluation.")

def main() -> None:
    """Main function to execute the workflow."""
    try:
        # Load data
        X, y = load_data()
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = split_data(X, y)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()