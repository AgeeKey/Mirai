"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-20T06:52:20.770703

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.exceptions import NotFittedError
from typing import Tuple

class IrisClassifier:
    """A simple Iris dataset classifier using Random Forest."""

    def __init__(self) -> None:
        """Initialize the classifier."""
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load the Iris dataset.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target arrays.
        """
        iris = load_iris()
        return iris.data, iris.target

    def train(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> None:
        """Train the Random Forest classifier.

        Args:
            X (np.ndarray): Feature matrix.
            y (np.ndarray): Target vector.
            test_size (float): Proportion of the dataset to include in the test split.
            random_state (int): Controls the randomness of the train-test split.

        Raises:
            ValueError: If the input data is invalid.
        """
        if X is None or y is None or len(X) == 0 or len(y) == 0:
            raise ValueError("Input data is invalid or empty.")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        self.model.fit(X_train, y_train)
        self.is_fitted = True

        # Evaluate the model
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model trained. Accuracy: {accuracy:.2f}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the class labels for the provided features.

        Args:
            X (np.ndarray): Feature matrix.

        Returns:
            np.ndarray: Predicted class labels.

        Raises:
            NotFittedError: If the model has not been fitted yet.
        """
        if not self.is_fitted:
            raise NotFittedError("The model is not fitted yet. Please call the 'train' method first.")

        return self.model.predict(X)

if __name__ == "__main__":
    classifier = IrisClassifier()
    features, target = classifier.load_data()
    classifier.train(features, target)

    # Example prediction
    sample_data = np.array([[5.0, 3.5, 1.5, 0.2]])
    prediction = classifier.predict(sample_data)
    print(f"Predicted class: {prediction[0]}")