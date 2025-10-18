"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-18T05:02:10.011248

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

class IrisClassifier:
    """A simple Random Forest Classifier for the Iris dataset."""
    
    def __init__(self) -> None:
        self.model = RandomForestClassifier()
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model with the training data."""
        try:
            self.model.fit(X_train, y_train)
        except ValueError as e:
            raise ValueError(f"Training failed: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the class labels for the provided features."""
        try:
            return self.model.predict(X)
        except NotFittedError as e:
            raise RuntimeError("The model is not fitted yet. Please train the model before predicting.") from e

def main() -> None:
    """Main function to execute the Iris classification workflow."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = split_data(features, target)
    
    classifier = IrisClassifier()
    classifier.train(X_train, y_train)
    
    predictions = classifier.predict(X_test)
    
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, predictions))

if __name__ == "__main__":
    main()