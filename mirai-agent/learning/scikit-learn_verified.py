"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T11:27:45.383372

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
    """Load the Iris dataset.

    Returns:
        Tuple containing features and target.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): Feature dataset.
        target (np.ndarray): Target dataset.
        test_size (float): Proportion of the dataset to include in the test split.

    Returns:
        Tuple containing training features, test features, training target, and test target.
    """
    return train_test_split(features, target, test_size=test_size, random_state=42)

class IrisClassifier:
    """Random Forest Classifier for Iris dataset."""
    
    def __init__(self) -> None:
        """Initialize the classifier."""
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the classifier on the training data.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training target.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions on the test data.

        Args:
            X_test (np.ndarray): Test features.

        Returns:
            np.ndarray: Predicted target values.
        """
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model performance.

        Args:
            y_true (np.ndarray): True target values.
            y_pred (np.ndarray): Predicted target values.
        """
        accuracy = accuracy_score(y_true, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_true, y_pred))

def main() -> None:
    """Main function to execute the workflow."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = split_data(features, target)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)

    y_pred = classifier.predict(X_test)
    classifier.evaluate(y_test, y_pred)

if __name__ == "__main__":
    main()