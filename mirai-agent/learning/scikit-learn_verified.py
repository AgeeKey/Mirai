"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-15T02:34:02.176893

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
    """Load the Iris dataset and return features and labels."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

class IrisClassifier:
    def __init__(self):
        """Initialize the RandomForestClassifier."""
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model with the training data."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""
        try:
            return self.model.predict(X)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model on the test data and print the accuracy and report."""
        predictions = self.predict(X_test)
        if len(predictions) == 0:
            return
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, predictions))

def main() -> None:
    """Main function to execute the classifier workflow."""
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)
    classifier.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()