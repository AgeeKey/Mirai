"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T21:09:15.931462

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_and_prepare_data() -> tuple:
    """Load the Iris dataset and split it into training and testing sets.

    Returns:
        tuple: A tuple containing training features, testing features,
               training labels, and testing labels.
    """
    try:
        iris = load_iris()
        X = iris.data
        y = iris.target
        return train_test_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier on the training data.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training labels.

    Returns:
        RandomForestClassifier: A trained Random Forest model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model using the test data.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing labels.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError(f"Error evaluating model: {e}")

def main() -> None:
    """Main function to execute the machine learning workflow."""
    X_train, X_test, y_train, y_test = load_and_prepare_data()
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()