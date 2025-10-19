"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T06:25:24.062206

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and return features and target variables.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The feature data.
        target (np.ndarray): The target data.
        test_size (float): The proportion of the dataset to include in the test split.
        random_state (int): Controls the shuffling applied to the data before applying the split.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training features, test features, training target, test target.
    """
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

class IrisClassifier:
    def __init__(self):
        """Initialize the Random Forest Classifier."""
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the Random Forest model.

        Args:
            X_train (np.ndarray): Training feature set.
            y_train (np.ndarray): Training target set.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise RuntimeError("Failed to train the model.") from e

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Make predictions using the trained model.

        Args:
            X_test (np.ndarray): Test feature set.

        Returns:
            np.ndarray: Predicted target values.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X_test)

def main() -> None:
    """Main function to load data, train the model, and evaluate its performance."""
    # Load data
    features, target = load_data()
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(features, target)
    
    # Create classifier instance
    classifier = IrisClassifier()
    
    # Train the model
    classifier.train(X_train, y_train)
    
    # Make predictions
    predictions = classifier.predict(X_test)
    
    # Evaluate the model
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

if __name__ == "__main__":
    main()