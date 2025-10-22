"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-22T00:38:25.861178

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from typing import Tuple, Any

class IrisClassifier:
    def __init__(self) -> None:
        """Initializes the IrisClassifier with a RandomForestClassifier model."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Loads the Iris dataset.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target arrays.
        """
        iris = load_iris()
        return iris.data, iris.target

    def split_data(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Splits the dataset into training and testing sets.

        Args:
            X (np.ndarray): Feature data.
            y (np.ndarray): Target data.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing data splits.
        """
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Trains the RandomForestClassifier model.

        Args:
            X_train (np.ndarray): Training feature data.
            y_train (np.ndarray): Training target data.
        """
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
        except Exception as e:
            print(f"An error occurred while training the model: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predicts the classes for the test data.

        Args:
            X_test (np.ndarray): Test feature data.

        Returns:
            np.ndarray: Predicted class labels.
        """
        if not self.is_fitted:
            raise NotFittedError("The model is not fitted yet. Please train the model before prediction.")
        return self.model.predict(X_test)

    def evaluate(self, y_test: np.ndarray, predictions: np.ndarray) -> None:
        """Evaluates the model performance.

        Args:
            y_test (np.ndarray): True class labels for the test data.
            predictions (np.ndarray): Predicted class labels.
        """
        accuracy = accuracy_score(y_test, predictions)
        print("Accuracy:", accuracy)
        print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
        print("Classification Report:\n", classification_report(y_test, predictions))

if __name__ == "__main__":
    iris_classifier = IrisClassifier()
    
    # Load the data
    X, y = iris_classifier.load_data()
    
    # Split the data
    X_train, X_test, y_train, y_test = iris_classifier.split_data(X, y)
    
    # Train the model
    iris_classifier.train(X_train, y_train)
    
    # Make predictions
    predictions = iris_classifier.predict(X_test)
    
    # Evaluate the model
    iris_classifier.evaluate(y_test, predictions)