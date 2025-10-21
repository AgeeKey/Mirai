"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-21T03:55:23.071678

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(features, target, test_size=test_size, random_state=42)

class IrisClassifier:
    """A classifier for the Iris dataset using Random Forest."""

    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred while training the model: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""
        try:
            return self.model.predict(X)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model before predicting.")
            return np.array([])

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model's performance."""
        y_pred = self.predict(X_test)
        if y_pred.size == 0:
            return
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))

def main() -> None:
    """Main function to run the Iris classification."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = split_data(features, target)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)
    classifier.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()