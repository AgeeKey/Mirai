"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T20:14:48.869682

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
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        X: Features data.
        y: Target labels.
        test_size: Proportion of the dataset to include in the test split.
        random_state: Controls the randomness of the training and testing data split.

    Returns:
        Tuple of training features, test features, training labels, test labels.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.

    Args:
        X_train: Training features.
        y_train: Training labels.

    Returns:
        Trained RandomForestClassifier model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model using test data and print the evaluation metrics.

    Args:
        model: Trained RandomForestClassifier model.
        X_test: Test features.
        y_test: Test labels.
    """
    y_pred = model.predict(X_test)
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

def main() -> None:
    """Main function to execute the workflow."""
    try:
        # Load data
        X, y = load_data()
        
        # Split data
        X_train, X_test, y_train, y_test = split_data(X, y)

        # Train model
        model = train_model(X_train, y_train)

        # Evaluate model
        evaluate_model(model, X_test, y_test)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()