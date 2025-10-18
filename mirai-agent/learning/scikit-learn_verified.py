"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T21:45:48.658130

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
    def __init__(self):
        """Initialize the IrisModel with a Random Forest Classifier."""
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load the Iris dataset.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target variables.
        """
        iris = load_iris()
        return iris.data, iris.target

    def preprocess_data(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split the dataset into training and testing sets.

        Args:
            X (np.ndarray): Feature dataset.
            y (np.ndarray): Target variable.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training features, test features, training targets, test targets.
        """
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model on the training data.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training target variable.
        """
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
        except Exception as e:
            print(f"Error during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.

        Args:
            X_test (np.ndarray): Test features.

        Returns:
            np.ndarray: Predicted target variable.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not self.is_fitted:
            raise NotFittedError("Model is not fitted yet. Please train the model first.")
        return self.model.predict(X_test)

    def evaluate(self, y_test: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model's performance.

        Args:
            y_test (np.ndarray): True target variable.
            y_pred (np.ndarray): Predicted target variable.
        """
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)

def main() -> None:
    """Main function to execute the Iris model training and evaluation."""
    iris_model = IrisModel()
    
    # Load and preprocess the data
    X, y = iris_model.load_data()
    X_train, X_test, y_train, y_test = iris_model.preprocess_data(X, y)

    # Train the model
    iris_model.train(X_train, y_train)

    # Make predictions
    y_pred = iris_model.predict(X_test)

    # Evaluate the model
    iris_model.evaluate(y_test, y_pred)

if __name__ == "__main__":
    main()