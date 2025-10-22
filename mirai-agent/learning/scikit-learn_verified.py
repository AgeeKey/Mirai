"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 1/1
Learned: 2025-10-22T18:46:11.110344

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError
from typing import Any, Tuple

class IrisClassifier:
    def __init__(self) -> None:
        """Initialize the IrisClassifier with a RandomForest model."""
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load the Iris dataset and return features and target labels.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target labels.
        """
        iris = load_iris()
        return iris.data, iris.target

    def split_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split the dataset into training and testing sets.

        Args:
            X (np.ndarray): Feature data.
            y (np.ndarray): Target labels.
            test_size (float): Proportion of the dataset to include in the test split.
            random_state (int): Random seed.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split data.
        """
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the RandomForest model on the training data.

        Args:
            X_train (np.ndarray): Training feature data.
            y_train (np.ndarray): Training target labels.
        """
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions on the test data.

        Args:
            X_test (np.ndarray): Test feature data.

        Returns:
            np.ndarray: Predicted labels.
        """
        if not self.is_fitted:
            raise NotFittedError("The model must be fitted before making predictions.")
        return self.model.predict(X_test)

    def evaluate(self, y_test: np.ndarray, predictions: np.ndarray) -> None:
        """Evaluate the model's performance.

        Args:
            y_test (np.ndarray): True labels for the test data.
            predictions (np.ndarray): Predicted labels from the model.
        """
        print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
        print("\nClassification Report:\n", classification_report(y_test, predictions))

def main() -> None:
    """Main function to run the Iris Classifier."""
    iris_classifier = IrisClassifier()
    
    # Load and split the data
    X, y = iris_classifier.load_data()
    X_train, X_test, y_train, y_test = iris_classifier.split_data(X, y)
    
    # Train the model
    iris_classifier.train(X_train, y_train)
    
    # Make predictions
    predictions = iris_classifier.predict(X_test)
    
    # Evaluate the model
    iris_classifier.evaluate(y_test, predictions)

if __name__ == "__main__":
    main()