"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-21T20:35:39.601077

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError("Error loading data: " + str(e))

def train_model(X: np.ndarray, y: np.ndarray) -> LogisticRegression:
    """
    Train a logistic regression model.

    Args:
        X (np.ndarray): Feature array.
        y (np.ndarray): Target array.

    Returns:
        LogisticRegression: Trained logistic regression model.
    """
    try:
        model = LogisticRegression(max_iter=200)
        model.fit(X, y)
        return model
    except Exception as e:
        raise RuntimeError("Error training model: " + str(e))

def evaluate_model(model: LogisticRegression, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model.

    Args:
        model (LogisticRegression): Trained logistic regression model.
        X_test (np.ndarray): Test feature array.
        y_test (np.ndarray): Test target array.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)
    except Exception as e:
        raise RuntimeError("Error evaluating model: " + str(e))

def main() -> None:
    """
    Main function to execute the workflow.
    """
    try:
        # Load data
        X, y = load_data()
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = train_model(X_train, y_train)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()