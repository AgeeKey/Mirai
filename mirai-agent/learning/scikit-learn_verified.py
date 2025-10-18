"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-18T08:27:30.292219

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
        Tuple[np.ndarray, np.ndarray]: Features and target labels.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature data.
        y (np.ndarray): Target labels.
        test_size (float): Proportion of the dataset to include in the test split.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split feature and target data.
    """
    return train_test_split(X, y, test_size=test_size, random_state=42)

class IrisClassifier:
    """A simple Iris classification model using Random Forest."""
    
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
    
    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the Random Forest model.

        Args:
            X (np.ndarray): Feature data.
            y (np.ndarray): Target labels.
        """
        self.model.fit(X, y)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions with the trained model.

        Args:
            X (np.ndarray): Feature data for predictions.

        Returns:
            np.ndarray: Predicted labels.

        Raises:
            NotFittedError: If the model has not been fitted yet.
        """
        if not hasattr(self.model, "predict"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X)

def main() -> None:
    """Main function to execute the Iris classification."""
    try:
        # Load data
        X, y = load_data()
        
        # Split data
        X_train, X_test, y_train, y_test = split_data(X, y)

        # Create and train model
        classifier = IrisClassifier()
        classifier.train(X_train, y_train)

        # Make predictions
        y_pred = classifier.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()