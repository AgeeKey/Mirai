"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-22T10:46:13.439140

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): Feature data.
        target (np.ndarray): Target data.
        test_size (float): Fraction of data to use as test set.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing features and target sets.
    """
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.

    Args:
        X_train (np.ndarray): Training feature set.
        y_train (np.ndarray): Training target set.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print accuracy and classification report.

    Args:
        model (RandomForestClassifier): Trained Random Forest model.
        X_test (np.ndarray): Testing feature set.
        y_test (np.ndarray): Testing target set.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to run the machine learning pipeline."""
    try:
        # Load data
        features, target = load_data()

        # Split data
        X_train, X_test, y_train, y_test = split_data(features, target)

        # Train model
        model = train_model(X_train, y_train)

        # Evaluate model
        evaluate_model(model, X_test, y_test)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()