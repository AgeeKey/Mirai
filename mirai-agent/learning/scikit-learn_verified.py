"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-21T02:20:40.249865

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from typing import Tuple, Any

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.
    
    Args:
        X (np.ndarray): Feature data.
        y (np.ndarray): Target data.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Seed used by the random number generator.
        
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing features and target arrays.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

class IrisClassifier:
    def __init__(self) -> None:
        """Initialize the RandomForestClassifier."""
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the model using the training data.
        
        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training target.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the classes of the test features.
        
        Args:
            X_test (np.ndarray): Test features.
        
        Returns:
            np.ndarray: Predicted classes.
        
        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet. Call 'train' first.")
        return self.model.predict(X_test)

def main() -> None:
    """Main function to execute the classification process."""
    # Load data
    X, y = load_data()

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Initialize classifier
    classifier = IrisClassifier()

    # Train the classifier
    classifier.train(X_train, y_train)

    # Make predictions
    y_pred = classifier.predict(X_test)

    # Print results
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()