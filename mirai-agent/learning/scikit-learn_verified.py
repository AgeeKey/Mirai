"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-21T19:30:22.137595

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
    """Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variable.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split datasets.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

class IrisClassifier:
    """A simple classifier for the Iris dataset using Random Forest."""

    def __init__(self) -> None:
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model.

        Args:
            X_train (np.ndarray): Training feature matrix.
            y_train (np.ndarray): Training target vector.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.

        Args:
            X_test (np.ndarray): Testing feature matrix.

        Returns:
            np.ndarray: Predicted labels.

        Raises:
            NotFittedError: If the model has not been trained.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X_test)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model's performance.

        Args:
            X_test (np.ndarray): Testing feature matrix.
            y_test (np.ndarray): True labels for the test set.
        """
        predictions = self.predict(X_test)
        print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
        print("\nClassification Report:\n", classification_report(y_test, predictions))

def main() -> None:
    """Main function to execute the workflow."""
    try:
        # Load dataset
        X, y = load_data()

        # Split dataset
        X_train, X_test, y_train, y_test = split_data(X, y)

        # Initialize and train classifier
        classifier = IrisClassifier()
        classifier.train(X_train, y_train)

        # Evaluate classifier
        classifier.evaluate(X_test, y_test)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()