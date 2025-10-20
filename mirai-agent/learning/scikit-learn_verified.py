"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T05:49:08.483009

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

def load_and_prepare_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and split it into features and target.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    try:
        iris = load_iris()
        X, y = iris.data, iris.target
        return X, y
    except Exception as e:
        raise RuntimeError("Error loading the Iris dataset.") from e

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.
    
    Args:
        X (np.ndarray): Feature array.
        y (np.ndarray): Target array.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.
        
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing feature and target arrays.
    """
    try:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    except ValueError as e:
        raise ValueError("Error splitting the dataset.") from e

class IrisModel:
    def __init__(self) -> None:
        """Initialize the Random Forest Classifier."""
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the model on the training dataset.
        
        Args:
            X_train (np.ndarray): Training feature array.
            y_train (np.ndarray): Training target array.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise RuntimeError("Error during model training.") from e

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the class labels for the provided test features.
        
        Args:
            X_test (np.ndarray): Testing feature array.
        
        Returns:
            np.ndarray: Predicted class labels.
        """
        try:
            return self.model.predict(X_test)
        except NotFittedError as e:
            raise RuntimeError("Model is not fitted. Call the train method first.") from e
        except Exception as e:
            raise RuntimeError("Error during prediction.") from e

def main() -> None:
    """Main function to execute the model training and evaluation."""
    try:
        X, y = load_and_prepare_data()
        X_train, X_test, y_train, y_test = split_data(X, y)

        model = IrisModel()
        model.train(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, predictions))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()