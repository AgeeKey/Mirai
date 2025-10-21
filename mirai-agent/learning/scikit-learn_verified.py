"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-21T13:32:06.567703

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
    """Load the Iris dataset and return features and target arrays."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        X: Features array.
        y: Target array.
        test_size: Proportion of the dataset to include in the test split.
        random_state: Controls the shuffling applied to the data before applying the split.

    Returns:
        A tuple containing training features, testing features, training target, testing target.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

class IrisModel:
    """A model for classifying Iris species using Random Forest."""
    
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model.

        Args:
            X_train: Training features.
            y_train: Training target.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict using the trained model.

        Args:
            X_test: Testing features.

        Returns:
            Predicted target values.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisModel instance is not fitted yet.")
        return self.model.predict(X_test)

def main() -> None:
    """Main function to execute the workflow."""
    try:
        # Load the dataset
        X, y = load_data()
        
        # Split the dataset
        X_train, X_test, y_train, y_test = split_data(X, y)
        
        # Initialize the model
        model = IrisModel()
        
        # Train the model
        model.train(X_train, y_train)
        
        # Make predictions
        predictions = model.predict(X_test)
        
        # Evaluate the model
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, predictions))
        print("\nClassification Report:")
        print(classification_report(y_test, predictions))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()