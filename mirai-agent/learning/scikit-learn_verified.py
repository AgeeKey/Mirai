"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-18T06:21:06.074657

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
        """Initializes the IrisModel with a RandomForestClassifier."""
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Loads the Iris dataset and returns features and target labels.
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target labels from the dataset.
        """
        iris = load_iris()
        return iris.data, iris.target

    def split_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Splits the dataset into training and testing sets.
        
        Args:
            X (np.ndarray): Feature data.
            y (np.ndarray): Target labels.
            test_size (float): Proportion of the dataset to include in the test split.
            random_state (int): Controls the randomness of the split.
        
        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing data.
        """
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Trains the model using the training data.
        
        Args:
            X_train (np.ndarray): Training feature data.
            y_train (np.ndarray): Training target labels.
        """
        self.model.fit(X_train, y_train)
        self.is_fitted = True

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Makes predictions on the test data.
        
        Args:
            X_test (np.ndarray): Test feature data.
        
        Returns:
            np.ndarray: Predicted labels.
        
        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not self.is_fitted:
            raise NotFittedError("The model is not fitted yet. Call 'train' before 'predict'.")
        return self.model.predict(X_test)

    def evaluate(self, y_test: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluates the model's performance and prints the accuracy and classification report.
        
        Args:
            y_test (np.ndarray): True labels for the test set.
            y_pred (np.ndarray): Predicted labels for the test set.
        """
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to execute the Iris model training and evaluation."""
    iris_model = IrisModel()
    
    # Load data
    X, y = iris_model.load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = iris_model.split_data(X, y)
    
    # Train the model
    iris_model.train(X_train, y_train)
    
    # Make predictions
    y_pred = iris_model.predict(X_test)
    
    # Evaluate the model
    iris_model.evaluate(y_test, y_pred)

if __name__ == "__main__":
    main()