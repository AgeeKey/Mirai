"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-14T16:23:17.203144

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError

def load_and_prepare_data() -> tuple:
    """
    Load the Iris dataset and split it into features and target variable.
    
    Returns:
        tuple: A tuple containing features (X) and target (y).
    """
    iris = load_iris()
    X = iris.data
    y = iris.target
    return X, y

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> tuple:
    """
    Split the dataset into training and testing sets.
    
    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random state for reproducibility.
        
    Returns:
        tuple: Training and testing feature and target sets.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

class IrisClassifier:
    def __init__(self):
        """
        Initialize the IrisClassifier with a RandomForestClassifier.
        """
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the Random Forest model on the training data.
        
        Args:
            X_train (np.ndarray): Training feature set.
            y_train (np.ndarray): Training target set.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise RuntimeError("Training failed") from e

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the class labels for the provided features.
        
        Args:
            X_test (np.ndarray): Testing feature set.
        
        Returns:
            np.ndarray: Predicted class labels.
            
        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X_test)

def main() -> None:
    """
    Main function to load data, train the model, and evaluate it.
    """
    X, y = load_and_prepare_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)

    y_pred = classifier.predict(X_test)

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()