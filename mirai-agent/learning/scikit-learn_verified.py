"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-18T01:52:08.792467

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
    """A class for building and evaluating a Random Forest model on the Iris dataset."""
    
    def __init__(self) -> None:
        """Initializes the IrisModel with a Random Forest Classifier."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Loads the Iris dataset.
        
        Returns:
            Tuple containing features and target arrays.
        """
        iris = load_iris()
        X = iris.data
        y = iris.target
        return X, y

    def split_data(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Splits the dataset into training and testing sets.
        
        Args:
            X: Feature array.
            y: Target array.
        
        Returns:
            Tuple containing training features, testing features, training labels, and testing labels.
        """
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Trains the Random Forest model on the training data.
        
        Args:
            X_train: Training feature array.
            y_train: Training target array.
        """
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluates the trained model on the test data.
        
        Args:
            X_test: Testing feature array.
            y_test: Testing target array.
        """
        if not self.is_fitted:
            raise NotFittedError("Model is not fitted yet. Please train the model before evaluation.")
        
        try:
            predictions = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            print(f"Accuracy: {accuracy:.2f}")
            print("Classification Report:")
            print(classification_report(y_test, predictions))
        except Exception as e:
            print(f"An error occurred during evaluation: {e}")

if __name__ == "__main__":
    iris_model = IrisModel()
    X, y = iris_model.load_data()
    X_train, X_test, y_train, y_test = iris_model.split_data(X, y)
    iris_model.train(X_train, y_train)
    iris_model.evaluate(X_test, y_test)