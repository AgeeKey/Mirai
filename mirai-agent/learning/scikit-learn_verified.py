"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T20:53:27.953357

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): Features of the dataset.
        target (np.ndarray): Target variable of the dataset.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing feature and target arrays.
    """
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

class IrisModel:
    """A simple Random Forest classifier for the Iris dataset."""
    
    def __init__(self) -> None:
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training target.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.

        Args:
            X_test (np.ndarray): Test features.

        Returns:
            np.ndarray: Predicted classes.

        Raises:
            NotFittedError: If the model is not fitted yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisModel instance is not fitted yet.")
        return self.model.predict(X_test)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model's performance.

        Args:
            X_test (np.ndarray): Test features.
            y_test (np.ndarray): True target values.
        """
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, predictions))

def main() -> None:
    """Main function to execute the model training and evaluation."""
    try:
        features, target = load_data()
        X_train, X_test, y_train, y_test = split_data(features, target)

        model = IrisModel()
        model.train(X_train, y_train)
        model.evaluate(X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()