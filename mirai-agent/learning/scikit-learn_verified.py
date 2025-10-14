"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-14T23:25:53.827474

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
    """Load the iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(features, target, test_size=test_size, random_state=42)

class IrisModel:
    """A simple Random Forest Classifier for the iris dataset."""
    
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model on the training data."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the target for the given features."""
        try:
            return self.model.predict(X)
        except NotFittedError:
            raise RuntimeError("Model is not fitted yet. Please call 'train' before 'predict'.")
        except Exception as e:
            print(f"An error occurred during prediction: {e}")
            return np.array([])

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model and print the accuracy and classification report."""
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print(classification_report(y_test, predictions))

def main() -> None:
    """Main function to run the model training and evaluation."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = split_data(features, target)

    model = IrisModel()
    model.train(X_train, y_train)
    model.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()