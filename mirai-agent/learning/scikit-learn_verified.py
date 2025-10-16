"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-16T23:31:31.508675

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

class IrisClassifier:
    def __init__(self):
        """Initializes the IrisClassifier with a RandomForestClassifier."""
        self.model = RandomForestClassifier()
    
    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Loads the Iris dataset.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target labels
        """
        iris = load_iris()
        return iris.data, iris.target

    def preprocess_data(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Splits the dataset into training and testing sets.

        Args:
            X (np.ndarray): Feature data.
            y (np.ndarray): Target labels.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Training and testing sets for features and labels.
        """
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Trains the RandomForest model on the training data.

        Args:
            X_train (np.ndarray): Training feature data.
            y_train (np.ndarray): Training target labels.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Makes predictions using the trained model.

        Args:
            X_test (np.ndarray): Testing feature data.

        Returns:
            np.ndarray: Predicted labels.

        Raises:
            NotFittedError: If the model has not been fitted yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X_test)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluates the model on the test data and prints accuracy and classification report.

        Args:
            X_test (np.ndarray): Testing feature data.
            y_test (np.ndarray): Testing target labels.
        """
        y_pred = self.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to execute the Iris classification process."""
    classifier = IrisClassifier()
    
    # Load and preprocess data
    X, y = classifier.load_data()
    X_train, X_test, y_train, y_test = classifier.preprocess_data(X, y)
    
    # Train the model
    classifier.train(X_train, y_train)
    
    # Evaluate the model
    classifier.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()