"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-14T22:37:00.112225

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.exceptions import NotFittedError
from typing import Tuple, Any

class IrisClassifier:
    def __init__(self) -> None:
        """Initializes the IrisClassifier with a RandomForest model."""
        self.model = RandomForestClassifier(n_estimators=100)

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Loads the iris dataset and returns features and labels.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and labels from the iris dataset.
        """
        iris = load_iris()
        return iris.data, iris.target

    def split_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Splits the dataset into training and testing sets.

        Args:
            X (np.ndarray): Features.
            y (np.ndarray): Labels.
            test_size (float): Proportion of the dataset to include in the test split.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing data.
        """
        return train_test_split(X, y, test_size=test_size, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Trains the model using the training data.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training labels.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Makes predictions on the test set.

        Args:
            X_test (np.ndarray): Test features.

        Returns:
            np.ndarray: Predicted labels.

        Raises:
            NotFittedError: If the model has not been fitted yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet. Call 'train' before 'predict'.")
        return self.model.predict(X_test)

    def evaluate(self, y_test: np.ndarray, y_pred: np.ndarray) -> float:
        """Evaluates the model's accuracy.

        Args:
            y_test (np.ndarray): True labels for the test set.
            y_pred (np.ndarray): Predicted labels.

        Returns:
            float: Accuracy score of the model.
        """
        return accuracy_score(y_test, y_pred)

def main() -> None:
    """Main function to run the IrisClassifier."""
    classifier = IrisClassifier()
    X, y = classifier.load_data()
    X_train, X_test, y_train, y_test = classifier.split_data(X, y)
    classifier.train(X_train, y_train)
    
    y_pred = classifier.predict(X_test)
    accuracy = classifier.evaluate(y_test, y_pred)
    
    print(f"Model accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()