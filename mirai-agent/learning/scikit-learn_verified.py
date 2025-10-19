"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.75
Tests Passed: 0/1
Learned: 2025-10-19T12:12:47.619711

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from typing import Tuple

class IrisClassifier:
    def __init__(self) -> None:
        """Initialize the IrisClassifier with a RandomForest model."""
        self.model = RandomForestClassifier(n_estimators=100)
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load the Iris dataset and return features and target labels."""
        try:
            iris = load_iris()
            X, y = iris.data, iris.target
            return X, y
        except Exception as e:
            raise RuntimeError(f"Error loading data: {e}")
    
    def split_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split the dataset into training and testing sets."""
        try:
            return train_test_split(X, y, test_size=test_size, random_state=42)
        except Exception as e:
            raise ValueError(f"Error splitting data: {e}")

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the RandomForest classifier."""
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
        except Exception as e:
            raise RuntimeError(f"Error during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the class labels for the test set."""
        if not self.is_fitted:
            raise NotFittedError("The model must be fitted before calling predict.")
        try:
            return self.model.predict(X_test)
        except Exception as e:
            raise RuntimeError(f"Error during prediction: {e}")

    def evaluate(self, y_test: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model's performance and print the results."""
        try:
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)
            print(f"Accuracy: {accuracy:.2f}")
            print("Classification Report:\n", report)
        except Exception as e:
            raise RuntimeError(f"Error during evaluation: {e}")


if __name__ == "__main__":
    classifier = IrisClassifier()
    X, y = classifier.load_data()
    X_train, X_test, y_train, y_test = classifier.split_data(X, y)
    classifier.train(X_train, y_train)
    y_pred = classifier.predict(X_test)
    classifier.evaluate(y_test, y_pred)