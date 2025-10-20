"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T15:25:08.388528

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from typing import Tuple, Any

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(features: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Preprocess the data by splitting it into training and test sets.

    Args:
        features (np.ndarray): Feature data.
        target (np.ndarray): Target data.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Training and test sets for features and target.
    """
    return train_test_split(features, target, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model on the training data.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test data and print the results.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): Test target.
    """
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", classification_report(y_test, predictions))

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    try:
        features, target = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(features, target)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()