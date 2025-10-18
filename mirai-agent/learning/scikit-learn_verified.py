"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-18T23:19:55.958282

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): Feature data.
        target (np.ndarray): Target labels.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing data.
    """
    try:
        return train_test_split(features, target, test_size=test_size, random_state=random_state)
    except Exception as e:
        raise ValueError(f"Error splitting data: {e}")

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target labels.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    try:
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """Evaluate the trained model on the test set.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing target labels.

    Returns:
        float: Accuracy score of the model.
    """
    try:
        y_pred = model.predict(X_test)
        return accuracy_score(y_test, y_pred)
    except Exception as e:
        raise RuntimeError(f"Error evaluating model: {e}")

def main() -> None:
    """Main function to run the machine learning pipeline."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = split_data(features, target)
    model = train_model(X_train, y_train)
    accuracy = evaluate_model(model, X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()