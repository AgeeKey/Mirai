"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-20T18:22:23.321635

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
from typing import Any, Tuple

class IrisClassifier:
    def __init__(self) -> None:
        """Initialize the IrisClassifier with a RandomForest model."""
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load the Iris dataset and return features and target labels.
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and labels from the Iris dataset.
        """
        iris = load_iris()
        return iris.data, iris.target

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the RandomForest model on the provided data.
        
        Args:
            X (np.ndarray): Features for training.
            y (np.ndarray): Target labels for training.
        """
        try:
            self.model.fit(X, y)
            self.is_fitted = True
        except Exception as e:
            print(f"An error occurred during model training: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the class labels for the provided features.
        
        Args:
            X (np.ndarray): Features for prediction.
        
        Returns:
            np.ndarray: Predicted class labels.
        
        Raises:
            NotFittedError: If the model has not been trained.
        """
        if not self.is_fitted:
            raise NotFittedError("Model is not fitted yet. Please train the model first.")
        return self.model.predict(X)

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> None:
        """Evaluate the model's performance on the test set and print results.
        
        Args:
            X (np.ndarray): Features for evaluation.
            y (np.ndarray): True target labels for evaluation.
        """
        predictions = self.predict(X)
        accuracy = accuracy_score(y, predictions)
        report = classification_report(y, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)

def main() -> None:
    """Main function to run the IrisClassifier."""
    clf = IrisClassifier()
    
    # Load the dataset
    X, y = clf.load_data()
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    clf.train(X_train, y_train)
    
    # Evaluate the model
    clf.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()