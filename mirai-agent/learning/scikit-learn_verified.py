"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-19T07:44:09.893844

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
from typing import Tuple, Any

class IrisClassifier:
    def __init__(self) -> None:
        """Initializes the IrisClassifier with a RandomForestClassifier."""
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Loads the Iris dataset.

        Returns:
            Tuple of features and target arrays.
        """
        iris = load_iris()
        return iris.data, iris.target

    def split_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Splits the dataset into training and testing sets.

        Args:
            X: Features array.
            y: Target array.
            test_size: Proportion of the dataset to include in the test split.
            random_state: Controls the shuffling applied to the data before applying the split.

        Returns:
            Tuple containing training features, testing features, training labels, and testing labels.
        """
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Trains the RandomForestClassifier.

        Args:
            X_train: Training features.
            y_train: Training labels.
        """
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predicts the class labels for the provided features.

        Args:
            X: Features array for prediction.

        Returns:
            Array of predicted class labels.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not self.is_fitted:
            raise NotFittedError("The model is not fitted yet. Please train the model before predicting.")
        return self.model.predict(X)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluates the model performance on the test set.

        Args:
            X_test: Testing features.
            y_test: Testing labels.
        """
        try:
            predictions = self.predict(X_test)
            print(f"Accuracy: {accuracy_score(y_test, predictions)}")
            print("Classification Report:\n", classification_report(y_test, predictions))
        except Exception as e:
            print(f"An error occurred during evaluation: {e}")

def main() -> None:
    """Main function to execute the Iris classification workflow."""
    classifier = IrisClassifier()
    
    # Load and split the data
    X, y = classifier.load_data()
    X_train, X_test, y_train, y_test = classifier.split_data(X, y)

    # Train the model
    classifier.train(X_train, y_train)

    # Evaluate the model
    classifier.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()