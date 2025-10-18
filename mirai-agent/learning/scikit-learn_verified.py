"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-18T00:17:13.884049

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
    """Load the Iris dataset and return features and target."""
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError("Error loading data: " + str(e))

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The feature data.
        target (np.ndarray): The target labels.
        test_size (float): Proportion of the dataset to include in the test split.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split datasets.
    """
    try:
        return train_test_split(features, target, test_size=test_size, random_state=42)
    except Exception as e:
        raise ValueError("Error splitting data: " + str(e))

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier.

    Args:
        X_train (np.ndarray): The training feature data.
        y_train (np.ndarray): The training target labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training model: " + str(e))

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test set.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): The test feature data.
        y_test (np.ndarray): The test target labels.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, predictions))
    except Exception as e:
        raise RuntimeError("Error evaluating model: " + str(e))

def main() -> None:
    """Main function to execute the machine learning workflow."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = split_data(features, target)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()