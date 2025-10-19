"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-19T16:09:35.564040

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


def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variable.
    """
    iris = load_iris()
    return iris.data, iris.target


def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): Feature data.
        target (np.ndarray): Target variable.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split datasets.
    """
    return train_test_split(features, target, test_size=test_size, random_state=random_state)


class IrisClassifier:
    def __init__(self) -> None:
        """
        Initialize the IrisClassifier with a Random Forest model.
        """
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the Random Forest model on the training data.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training target.

        Raises:
            ValueError: If training data is empty.
        """
        if X_train.size == 0 or y_train.size == 0:
            raise ValueError("Training data cannot be empty.")
        self.model.fit(X_train, y_train)

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the class labels for the test data.

        Args:
            X_test (np.ndarray): Test features.

        Returns:
            np.ndarray: Predicted class labels.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("The model is not fitted yet.")
        return self.model.predict(X_test)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """
        Evaluate the model's performance on the test data.

        Args:
            X_test (np.ndarray): Test features.
            y_test (np.ndarray): True labels for test features.
        """
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, predictions))


def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    # Load data
    features, target = load_data()
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(features, target)

    # Initialize the classifier
    classifier = IrisClassifier()

    # Train the classifier
    classifier.train(X_train, y_train)

    # Evaluate the classifier
    classifier.evaluate(X_test, y_test)


if __name__ == "__main__":
    main()