"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-22T11:50:49.063069

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

class IrisClassifier:
    def __init__(self) -> None:
        """Initialize the IrisClassifier with a RandomForestClassifier model."""
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load the Iris dataset.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target labels.
        """
        iris = load_iris()
        return iris.data, iris.target

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the RandomForestClassifier model.

        Args:
            X (np.ndarray): Feature dataset.
            y (np.ndarray): Target labels.

        Raises:
            ValueError: If input arrays do not match in length.
        """
        if X.shape[0] != y.shape[0]:
            raise ValueError("Feature and target arrays must have the same number of samples.")
        
        self.model.fit(X, y)
        self.is_fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.

        Args:
            X (np.ndarray): Feature dataset for predictions.

        Returns:
            np.ndarray: Predicted labels.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not self.is_fitted:
            raise NotFittedError("Model is not fitted. Please call 'train' before 'predict'.")
        
        return self.model.predict(X)

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> None:
        """Evaluate the model performance.

        Args:
            X (np.ndarray): Feature dataset for evaluation.
            y (np.ndarray): True target labels.
        """
        y_pred = self.predict(X)
        print("Accuracy:", accuracy_score(y, y_pred))
        print("\nClassification Report:\n", classification_report(y, y_pred))


if __name__ == "__main__":
    try:
        # Initialize the classifier
        classifier = IrisClassifier()

        # Load the data
        X, y = classifier.load_data()

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the classifier
        classifier.train(X_train, y_train)

        # Evaluate the classifier
        classifier.evaluate(X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")