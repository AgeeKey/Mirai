"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.75
Tests Passed: 0/1
Learned: 2025-10-20T15:57:22.853825

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    try:
        return train_test_split(features, target, test_size=test_size, random_state=random_state)
    except Exception as e:
        raise ValueError("Error while splitting data: " + str(e))

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier on the training data."""
    model = RandomForestClassifier(random_state=42)
    try:
        model.fit(X_train, y_train)
    except Exception as e:
        raise ValueError("Error while training the model: " + str(e))
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test data."""
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except Exception as e:
        raise ValueError("Error while evaluating the model: " + str(e))

def main() -> None:
    """Main function to execute the workflow."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = split_data(features, target)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()