"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-14T21:48:31.012918

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
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
        raise RuntimeError("Failed to load data") from e

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing data.
    """
    try:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    except Exception as e:
        raise RuntimeError("Failed to split data") from e

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest model.

    Args:
        X_train (np.ndarray): Training feature matrix.
        y_train (np.ndarray): Training target vector.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Failed to train model") from e

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """
    Evaluate the trained model.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Testing feature matrix.
        y_test (np.ndarray): Testing target vector.

    Returns:
        float: Accuracy of the model.
    """
    try:
        y_pred = model.predict(X_test)
        return accuracy_score(y_test, y_pred)
    except Exception as e:
        raise RuntimeError("Failed to evaluate model") from e

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    try:
        X, y = load_data()  # Load data
        X_train, X_test, y_train, y_test = split_data(X, y)  # Split data
        model = train_model(X_train, y_train)  # Train model
        accuracy = evaluate_model(model, X_test, y_test)  # Evaluate model
        print(f"Model accuracy: {accuracy:.2f}")  # Print accuracy
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()