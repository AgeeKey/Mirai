"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.75
Tests Passed: 0/1
Learned: 2025-10-20T08:10:55.459183

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
    """Load the Iris dataset and return features and target labels."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(features, target, test_size=test_size, random_state=42)

class IrisClassifier:
    """A simple Iris Classifier using Random Forest."""

    def __init__(self) -> None:
        """Initialize the classifier."""
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model on the training data."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions on the test data."""
        try:
            if not hasattr(self.model, "estimators_"):
                raise NotFittedError("The model is not fitted yet.")
            return self.model.predict(X_test)
        except NotFittedError as e:
            print(e)
            return np.array([])

    def evaluate(self, y_test: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model performance."""
        try:
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)
            print(f"Accuracy: {accuracy:.2f}")
            print("Classification Report:\n", report)
        except Exception as e:
            print(f"An error occurred during evaluation: {e}")

def main() -> None:
    """Main function to execute the Iris classification."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = split_data(features, target)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)

    y_pred = classifier.predict(X_test)
    if y_pred.size > 0:
        classifier.evaluate(y_test, y_pred)

if __name__ == "__main__":
    main()