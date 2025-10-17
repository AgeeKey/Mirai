"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-17T16:45:47.461073

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target labels."""
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError(f"Error loading the dataset: {e}")

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    try:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    except ValueError as e:
        raise ValueError(f"Error in data splitting: {e}")

class IrisClassifier:
    def __init__(self):
        """Initialize the Random Forest Classifier."""
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model using the training data."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise RuntimeError(f"Error during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the labels for the test data."""
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            raise RuntimeError("Model is not fitted. Please train the model before prediction.")
        except Exception as e:
            raise RuntimeError(f"Error during prediction: {e}")

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model and print the accuracy and classification report."""
        accuracy = accuracy_score(y_true, y_pred)
        report = classification_report(y_true, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)

def main() -> None:
    """Main function to execute the classifier."""
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)
    
    y_pred = classifier.predict(X_test)
    classifier.evaluate(y_test, y_pred)

if __name__ == "__main__":
    main()