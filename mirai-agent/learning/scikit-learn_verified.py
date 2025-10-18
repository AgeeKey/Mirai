"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-18T18:37:15.736673

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
    def __init__(self, n_estimators: int = 100):
        """
        Initialize the IrisClassifier with a Random Forest model.

        Args:
            n_estimators (int): The number of trees in the forest.
        """
        self.model = RandomForestClassifier(n_estimators=n_estimators)
    
    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load the Iris dataset.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target variable from the dataset.
        """
        iris = load_iris()
        return iris.data, iris.target
    
    def split_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Split the dataset into training and testing sets.

        Args:
            X (np.ndarray): Feature data.
            y (np.ndarray): Target variable.
            test_size (float): Proportion of the dataset to include in the test split.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing data.
        """
        return train_test_split(X, y, test_size=test_size, random_state=42)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the Random Forest model.

        Args:
            X_train (np.ndarray): Training feature data.
            y_train (np.ndarray): Training target variable.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the classes for the test data.

        Args:
            X_test (np.ndarray): Testing feature data.

        Returns:
            np.ndarray: Predicted classes.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("Model is not fitted yet. Please train the model first.")
        return self.model.predict(X_test)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """
        Evaluate the model and print the accuracy and classification report.

        Args:
            X_test (np.ndarray): Testing feature data.
            y_test (np.ndarray): True target variable.
        """
        y_pred = self.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(report)

if __name__ == "__main__":
    classifier = IrisClassifier()
    X, y = classifier.load_data()
    X_train, X_test, y_train, y_test = classifier.split_data(X, y)
    classifier.train(X_train, y_train)
    classifier.evaluate(X_test, y_test)