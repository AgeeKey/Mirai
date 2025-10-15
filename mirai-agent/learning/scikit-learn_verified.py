"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-15T16:20:43.834370

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(features: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(features, target, test_size=0.2, random_state=42)

class IrisModel:
    def __init__(self) -> None:
        """Initialize the RandomForestClassifier model."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model using the training data."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise RuntimeError("Error training the model") from e

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions on the test data."""
        try:
            return self.model.predict(X_test)
        except NotFittedError as e:
            raise RuntimeError("Model is not fitted yet. Please train the model first.") from e
        except Exception as e:
            raise RuntimeError("Error making predictions") from e

    def evaluate(self, y_test: np.ndarray, predictions: np.ndarray) -> None:
        """Evaluate the model performance and print the classification report."""
        print(confusion_matrix(y_test, predictions))
        print(classification_report(y_test, predictions))

def main() -> None:
    """Main function to load data, train the model, and evaluate it."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(features, target)
    
    model = IrisModel()
    model.train(X_train, y_train)
    
    predictions = model.predict(X_test)
    model.evaluate(y_test, predictions)

if __name__ == "__main__":
    main()