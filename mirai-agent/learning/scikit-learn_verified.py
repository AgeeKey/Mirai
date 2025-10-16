"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T23:15:23.714748

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target.

    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing the features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(features: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The feature data.
        target (np.ndarray): The target labels.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split data: X_train, X_test, y_train, y_test.
    """
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.

    Args:
        X_train (np.ndarray): The training features.
        y_train (np.ndarray): The training labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to train the model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print metrics.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): The test features.
        y_test (np.ndarray): The test labels.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, predictions))
        print("Classification Report:")
        print(classification_report(y_test, predictions))
    except Exception as e:
        raise RuntimeError(f"Failed to evaluate the model: {e}")

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(features, target)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()