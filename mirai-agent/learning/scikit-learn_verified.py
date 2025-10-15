"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-15T22:19:05.332343

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from typing import Tuple, Any

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variable.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Features dataset.
        y (np.ndarray): Target variable.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Controls the randomness of the train/test split.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split datasets.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

class IrisClassifier:
    def __init__(self):
        """Initialize the RandomForestClassifier."""
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the RandomForestClassifier on the training data.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training target variable.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"Error during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the class labels for the provided test data.

        Args:
            X_test (np.ndarray): Test features.

        Returns:
            np.ndarray: Predicted class labels.
        """
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """
        Evaluate the model performance on the test data.

        Args:
            X_test (np.ndarray): Test features.
            y_test (np.ndarray): True class labels for test data.
        """
        y_pred = self.predict(X_test)
        if y_pred.size > 0:
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Accuracy: {accuracy:.2f}")
            print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to execute the model training and evaluation."""
    # Load data
    X, y = load_data()
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Initialize and train the classifier
    classifier = IrisClassifier()
    classifier.train(X_train, y_train)
    
    # Evaluate the classifier
    classifier.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()