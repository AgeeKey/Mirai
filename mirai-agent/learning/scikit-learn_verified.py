"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T15:55:43.182100

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

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): Feature matrix.
        target (np.ndarray): Target vector.
        test_size (float): Proportion of the dataset to include in the test split.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split feature and target sets.
    """
    return train_test_split(features, target, test_size=test_size, random_state=42)

class IrisClassifier:
    """A simple classifier for the Iris dataset using Random Forest."""

    def __init__(self):
        """Initialize the classifier."""
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest classifier.

        Args:
            X_train (np.ndarray): Training feature matrix.
            y_train (np.ndarray): Training target vector.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the class labels for the provided features.

        Args:
            X (np.ndarray): Feature matrix for predictions.

        Returns:
            np.ndarray: Predicted class labels.

        Raises:
            NotFittedError: If the model has not been fitted yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the classifier on the test set.

        Args:
            X_test (np.ndarray): Test feature matrix.
            y_test (np.ndarray): Test target vector.
        """
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)

        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)

def main() -> None:
    """Main function to run the Iris classification."""
    try:
        features, target = load_data()
        X_train, X_test, y_train, y_test = split_data(features, target)

        classifier = IrisClassifier()
        classifier.train(X_train, y_train)
        classifier.evaluate(X_test, y_test)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()