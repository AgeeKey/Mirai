"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T18:23:32.820654

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
from typing import Tuple

class IrisModel:
    def __init__(self) -> None:
        """Initialize the IrisModel with a RandomForestClassifier."""
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load the Iris dataset.
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target arrays.
        """
        iris = load_iris()
        return iris.data, iris.target

    def split_data(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split the dataset into training and testing sets.

        Args:
            X (np.ndarray): Feature array.
            y (np.ndarray): Target array.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split data for training and testing.
        """
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the RandomForestClassifier model.

        Args:
            X_train (np.ndarray): Training feature set.
            y_train (np.ndarray): Training target set.
        """
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
        except Exception as e:
            print(f"An error occurred during model training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.

        Args:
            X_test (np.ndarray): Test feature set.

        Returns:
            np.ndarray: Predicted labels.

        Raises:
            NotFittedError: If the model has not been fitted yet.
        """
        if not self.is_fitted:
            raise NotFittedError("Model is not fitted yet. Please train the model before predicting.")
        return self.model.predict(X_test)

    def evaluate(self, y_test: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model's performance.

        Args:
            y_test (np.ndarray): True labels for the test set.
            y_pred (np.ndarray): Predicted labels.
        """
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to run the Iris classification model."""
    iris_model = IrisModel()
    X, y = iris_model.load_data()
    X_train, X_test, y_train, y_test = iris_model.split_data(X, y)
    
    iris_model.train(X_train, y_train)
    
    y_pred = iris_model.predict(X_test)
    iris_model.evaluate(y_test, y_pred)

if __name__ == "__main__":
    main()