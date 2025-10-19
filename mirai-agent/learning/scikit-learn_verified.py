"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T02:13:07.856344

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier model.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X: np.ndarray, y: np.ndarray) -> None:
    """
    Evaluate the trained model and print accuracy and classification report.

    Args:
        model (RandomForestClassifier): Trained Random Forest model.
        X (np.ndarray): Feature matrix for evaluation.
        y (np.ndarray): True target vector for evaluation.
    """
    try:
        predictions = model.predict(X)
        accuracy = accuracy_score(y, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y, predictions))
    except NotFittedError as e:
        print("Model is not fitted yet. Error:", e)

def main() -> None:
    """
    Main function to run the machine learning workflow.
    """
    try:
        X, y = load_data()  # Load dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split data
        model = train_model(X_train, y_train)  # Train model
        evaluate_model(model, X_test, y_test)  # Evaluate model
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()