"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-22T13:28:18.098970

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
        """Initialize the IrisClassifier with a Random Forest model."""
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load the Iris dataset.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target variable from the dataset.
        """
        iris = load_iris()
        return iris.data, iris.target

    def split_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split the dataset into training and testing sets.

        Args:
            X (np.ndarray): Feature data.
            y (np.ndarray): Target data.
            test_size (float, optional): Proportion of the dataset to include in the test split.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training features, testing features, training labels, testing labels.
        """
        return train_test_split(X, y, test_size=test_size, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model.

        Args:
            X_train (np.ndarray): Training feature data.
            y_train (np.ndarray): Training target data.
        """
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.

        Args:
            X_test (np.ndarray): Testing feature data.

        Returns:
            np.ndarray: Predicted labels.

        Raises:
            NotFittedError: If the model has not been trained.
        """
        if not self.is_fitted:
            raise NotFittedError("The model is not fitted yet. Please train the model before predicting.")
        
        return self.model.predict(X_test)

    def evaluate(self, y_test: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model's performance.

        Args:
            y_test (np.ndarray): True labels for the test set.
            y_pred (np.ndarray): Predicted labels.
        """
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    classifier = IrisClassifier()
    
    # Load data
    X, y = classifier.load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = classifier.split_data(X, y)

    # Train model
    classifier.train(X_train, y_train)

    # Make predictions
    y_pred = classifier.predict(X_test)

    # Evaluate model
    classifier.evaluate(y_test, y_pred)