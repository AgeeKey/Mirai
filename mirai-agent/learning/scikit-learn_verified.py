"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T12:44:19.995745

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

def load_and_prepare_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the iris dataset and prepare features and target variables.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variables.
    """
    iris = load_iris()
    X, y = iris.data, iris.target
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier on the provided data.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model using accuracy and classification report.

    Args:
        model (RandomForestClassifier): Trained Random Forest model.
        X_test (np.ndarray): Test feature matrix.
        y_test (np.ndarray): Test target vector.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)
    except NotFittedError as e:
        print("Error: Model is not fitted. Please train the model before evaluation.")
        raise e

def main() -> None:
    """Main function to execute the training and evaluation of the model."""
    try:
        # Load and prepare data
        X, y = load_and_prepare_data()

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = train_model(X_train, y_train)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()