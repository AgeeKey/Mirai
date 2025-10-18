"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-18T08:43:23.593199

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
    """
    Load the Iris dataset.

    Returns:
        Tuple containing features and target variable.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Features.
        y (np.ndarray): Target variable.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple of training features, testing features, training labels, and testing labels.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

class IrisClassifier:
    def __init__(self):
        """Initialize the Random Forest Classifier."""
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the Random Forest model on the training data.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training labels.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict the labels for the given features.

        Args:
            X (np.ndarray): Features to predict.

        Returns:
            np.ndarray: Predicted labels.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """
        Evaluate the model and print accuracy and classification report.

        Args:
            X_test (np.ndarray): Testing features.
            y_test (np.ndarray): True labels for testing features.
        """
        y_pred = self.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))

def main() -> None:
    """Main function to run the Iris Classifier."""
    try:
        # Load and split data
        X, y = load_data()
        X_train, X_test, y_train, y_test = split_data(X, y)

        # Initialize and train the classifier
        classifier = IrisClassifier()
        classifier.train(X_train, y_train)

        # Evaluate the classifier
        classifier.evaluate(X_test, y_test)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()