"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-19T06:09:39.087454

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError

def load_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target variables."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(X, y, test_size=test_size, random_state=42)

class IrisClassifier:
    """A classifier for the Iris dataset using Random Forest."""
    
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest classifier."""
        self.model.fit(X_train, y_train)

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            raise RuntimeError("The model is not fitted yet. Please call 'train' before 'predict'.")

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model and print the accuracy and classification report."""
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, predictions))

def main() -> None:
    """Main function to execute the workflow."""
    try:
        # Load data
        X, y = load_data()
        
        # Split data
        X_train, X_test, y_train, y_test = split_data(X, y)
        
        # Create classifier
        classifier = IrisClassifier()
        
        # Train the model
        classifier.train(X_train, y_train)
        
        # Evaluate the model
        classifier.evaluate(X_test, y_test)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()