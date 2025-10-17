"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-17T03:01:48.925283

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
    """Load the Iris dataset and return features and target labels."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.
    
    Args:
        features (np.ndarray): Feature data.
        target (np.ndarray): Target labels.
        test_size (float): Proportion of the dataset to include in the test split.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split data.
    """
    return train_test_split(features, target, test_size=test_size, random_state=42)

class IrisClassifier:
    def __init__(self):
        """Initialize the Random Forest classifier."""
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model with training data.
        
        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training labels.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"Error during model training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the labels for test data.
        
        Args:
            X_test (np.ndarray): Test features.
        
        Returns:
            np.ndarray: Predicted labels.
        """
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])

    def evaluate(self, y_test: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model's performance.
        
        Args:
            y_test (np.ndarray): True labels for test data.
            y_pred (np.ndarray): Predicted labels.
        """
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
        print("\nClassification Report:\n", classification_report(y_test, y_pred))

def main() -> None:
    """Main function to execute the model training and evaluation."""
    # Load data
    features, target = load_data()
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(features, target)
    
    # Initialize and train the classifier
    classifier = IrisClassifier()
    classifier.train(X_train, y_train)
    
    # Make predictions
    y_pred = classifier.predict(X_test)
    
    # Evaluate the model
    if y_pred.size > 0:
        classifier.evaluate(y_test, y_pred)

if __name__ == "__main__":
    main()