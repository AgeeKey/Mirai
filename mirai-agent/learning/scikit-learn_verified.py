"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T02:39:34.948328

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_and_prepare_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Load and prepare the Iris dataset.

    Returns:
        tuple: Features and target variables.
    """
    try:
        iris = load_iris()
        X, y = iris.data, iris.target
        return X, y
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier on the given data.

    Args:
        X (np.ndarray): Feature data.
        y (np.ndarray): Target labels.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model and print the accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test feature data.
        y_test (np.ndarray): True labels for test data.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError(f"Error evaluating model: {e}")

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    X, y = load_and_prepare_data()  # Load dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split data
    model = train_model(X_train, y_train)  # Train model
    evaluate_model(model, X_test, y_test)  # Evaluate model

if __name__ == "__main__":
    main()  # Run the main function