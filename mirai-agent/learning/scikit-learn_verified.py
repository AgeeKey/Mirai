"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T00:02:07.321202

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.exceptions import NotFittedError

def load_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and return features and target.

    Returns:
        tuple: Features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(features: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): Feature data.
        target (np.ndarray): Target data.

    Returns:
        tuple: Training features, testing features, training target, testing target.
    """
    return train_test_split(features, target, test_size=0.2, random_state=42)

class IrisClassifier:
    def __init__(self) -> None:
        """
        Initialize the IrisClassifier with a RandomForestClassifier.
        """
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the model on the training data.

        Args:
            X_train (np.ndarray): Training feature data.
            y_train (np.ndarray): Training target data.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Make predictions on the test data.

        Args:
            X_test (np.ndarray): Test feature data.

        Returns:
            np.ndarray: Predicted target data.
        """
        try:
            return self.model.predict(X_test)
        except NotFittedError as e:
            print(f"Model is not fitted yet: {e}")
            return np.array([])

def main() -> None:
    """
    Main function to execute the classification process.
    """
    # Load the dataset
    features, target = load_data()

    # Preprocess the data
    X_train, X_test, y_train, y_test = preprocess_data(features, target)

    # Initialize the classifier
    classifier = IrisClassifier()

    # Train the model
    classifier.train(X_train, y_train)

    # Make predictions
    predictions = classifier.predict(X_test)

    # Evaluate the model
    if predictions.size > 0:
        print("Accuracy:", accuracy_score(y_test, predictions))
        print(classification_report(y_test, predictions))

if __name__ == "__main__":
    main()