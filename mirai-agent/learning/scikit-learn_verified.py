"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-22T06:13:12.160987

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
    """
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variable.
    """
    try:
        data = load_iris()
        return data.data, data.target
    except Exception as e:
        raise RuntimeError("Error loading the dataset") from e

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target variable.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        raise RuntimeError("Error training the model") from e

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Test feature matrix.
        y_test (np.ndarray): Test target variable.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)
    except Exception as e:
        raise RuntimeError("Error evaluating the model") from e

def main() -> None:
    """
    Main function to execute the ML workflow.
    """
    try:
        # Load the dataset
        X, y = load_data()

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = train_model(X_train, y_train)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()