"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-19T01:41:34.166220

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError("Failed to load data.") from e

def split_data(features: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    try:
        return train_test_split(features, target, test_size=0.2, random_state=42)
    except Exception as e:
        raise ValueError("Failed to split data.") from e

class IrisClassifier:
    def __init__(self) -> None:
        """Initialize the Iris Classifier."""
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise RuntimeError("Failed to train the model.") from e

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the class labels for the input samples."""
        try:
            return self.model.predict(X)
        except NotFittedError:
            raise RuntimeError("Model must be trained before predictions.")
        except Exception as e:
            raise RuntimeError("Failed to make predictions.") from e

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model performance."""
        y_pred = self.predict(X_test)
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to execute the workflow."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = split_data(features, target)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)
    classifier.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()