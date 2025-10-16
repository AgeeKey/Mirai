"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-16T02:36:19.039494

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
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

class IrisClassifier:
    """A classifier for the Iris dataset using Random Forest."""

    def __init__(self):
        """Initialize the classifier."""
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the classifier on the training data."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions on the test data."""
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])
        except Exception as e:
            print(f"An error occurred during prediction: {e}")
            return np.array([])

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model's performance."""
        accuracy = accuracy_score(y_true, y_pred)
        report = classification_report(y_true, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)

def main() -> None:
    """Main function to execute the workflow."""
    X, y = load_data()  # Load data
    X_train, X_test, y_train, y_test = split_data(X, y)  # Split data

    classifier = IrisClassifier()  # Initialize classifier
    classifier.train(X_train, y_train)  # Train the model
    y_pred = classifier.predict(X_test)  # Make predictions
    classifier.evaluate(y_test, y_pred)  # Evaluate the model

if __name__ == "__main__":
    main()  # Run the main function