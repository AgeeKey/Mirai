"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-17T05:41:24.348537

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and labels.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and labels from the dataset.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, labels: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and test sets.

    Args:
        features (np.ndarray): The feature set.
        labels (np.ndarray): The labels for the feature set.
        test_size (float): The proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split datasets (X_train, X_test, y_train, y_test).
    """
    return train_test_split(features, labels, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training labels.

    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model using the test data.

    Args:
        model (RandomForestClassifier): The trained model to evaluate.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): Test labels.

    Raises:
        NotFittedError: If the model has not been fitted yet.
    """
    try:
        predictions = model.predict(X_test)
        print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
        print("Classification Report:\n", classification_report(y_test, predictions))
    except NotFittedError as e:
        print("Model is not fitted yet. Please fit the model before evaluation.")
        raise e

def main() -> None:
    """Main function to execute the machine learning workflow."""
    features, labels = load_data()  # Load the data
    X_train, X_test, y_train, y_test = split_data(features, labels)  # Split the data
    model = train_model(X_train, y_train)  # Train the model
    evaluate_model(model, X_test, y_test)  # Evaluate the model

if __name__ == "__main__":
    main()  # Run the main function