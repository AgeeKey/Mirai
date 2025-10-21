"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-21T09:45:44.432549

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.exceptions import NotFittedError

def load_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target.

    Returns:
        tuple: Features and target arrays from the dataset.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The feature data.
        target (np.ndarray): The target labels.
        test_size (float): The proportion of the dataset to include in the test split.

    Returns:
        tuple: Training features, test features, training target, test target.
    """
    return train_test_split(features, target, test_size=test_size, random_state=42)

class IrisClassifier:
    """A classifier for the Iris dataset using Random Forest."""
    
    def __init__(self) -> None:
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training target labels.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the labels for test data.

        Args:
            X_test (np.ndarray): Test features.

        Returns:
            np.ndarray: Predicted labels.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X_test)

def main() -> None:
    """Main function to run the Iris classification."""
    try:
        # Load data
        features, target = load_data()
        
        # Split data
        X_train, X_test, y_train, y_test = split_data(features, target)
        
        # Initialize classifier
        classifier = IrisClassifier()
        
        # Train the model
        classifier.train(X_train, y_train)
        
        # Make predictions
        predictions = classifier.predict(X_test)
        
        # Evaluate the model
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        
        # Print results
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(report)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()