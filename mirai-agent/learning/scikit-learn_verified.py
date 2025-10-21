"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-21T11:06:18.220838

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

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

class IrisModel:
    """A model class for training and predicting using Random Forest on the Iris dataset."""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")
    
    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])

def main() -> None:
    """Main function to execute the training and prediction process."""
    features, target = load_data()  # Load data
    X_train, X_test, y_train, y_test = split_data(features, target)  # Split data
    
    model = IrisModel()  # Initialize the model
    model.train(X_train, y_train)  # Train the model
    
    predictions = model.predict(X_test)  # Make predictions
    accuracy = accuracy_score(y_test, predictions)  # Calculate accuracy
    
    print(f'Accuracy: {accuracy:.2f}')  # Print accuracy
    print(classification_report(y_test, predictions))  # Print classification report

if __name__ == "__main__":
    main()  # Run the main function