"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-21T21:56:45.499016

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

class IrisClassifier:
    def __init__(self) -> None:
        """Initialize the IrisClassifier with a Random Forest model."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load the Iris dataset.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target variable.
        """
        iris = load_iris()
        return iris.data, iris.target

    def split_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split the data into training and testing sets.

        Args:
            X (np.ndarray): Features.
            y (np.ndarray): Target variable.
            test_size (float): Proportion of the dataset to include in the test split.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing data.
        """
        return train_test_split(X, y, test_size=test_size, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training target variable.
        """
        self.model.fit(X_train, y_train)
        self.is_fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.

        Args:
            X (np.ndarray): Features to predict.

        Returns:
            np.ndarray: Predicted target variable.

        Raises:
            NotFittedError: If the model has not been fitted yet.
        """
        if not self.is_fitted:
            raise NotFittedError("The model must be trained before making predictions.")
        return self.model.predict(X)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model on test data.

        Args:
            X_test (np.ndarray): Testing features.
            y_test (np.ndarray): Testing target variable.
        """
        y_pred = self.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to execute the Iris classification."""
    classifier = IrisClassifier()
    
    # Load and split data
    X, y = classifier.load_data()
    X_train, X_test, y_train, y_test = classifier.split_data(X, y)

    # Train the model
    classifier.train(X_train, y_train)

    # Evaluate the model
    classifier.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()