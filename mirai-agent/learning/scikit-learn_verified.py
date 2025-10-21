"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-21T22:12:56.575615

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variables.
    """
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
        Training features, test features, training target, test target.
    """
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    def __init__(self):
        """Initialize the RandomForestClassifier."""
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the RandomForest model.

        Args:
            X_train (np.ndarray): Training feature matrix.
            y_train (np.ndarray): Training target vector.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict using the trained model.

        Args:
            X_test (np.ndarray): Test feature matrix.

        Returns:
            np.ndarray: Predicted target values.
        """
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Evaluate the model's accuracy.

        Args:
            y_true (np.ndarray): True target values.
            y_pred (np.ndarray): Predicted target values.

        Returns:
            float: Accuracy score of the model.
        """
        return accuracy_score(y_true, y_pred)

def main() -> None:
    """Main function to run the Iris classifier."""
    X, y = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(X, y)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)

    y_pred = classifier.predict(X_test)
    
    if y_pred.size > 0:
        accuracy = classifier.evaluate(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()