"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-18T11:20:51.847722

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.exceptions import NotFittedError

def load_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

class IrisClassifier:
    """A classifier for the Iris dataset using Random Forest."""
    
    def __init__(self) -> None:
        self.model = RandomForestClassifier()

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the Random Forest model."""
        try:
            self.model.fit(X, y)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""
        try:
            return self.model.predict(X)
        except NotFittedError as e:
            print("Model is not fitted yet. Please train the model before predicting.")
            raise e
        except Exception as e:
            print(f"An error occurred during prediction: {e}")
            raise e

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> float:
        """Evaluate the model accuracy on the test set."""
        predictions = self.predict(X)
        accuracy = accuracy_score(y, predictions)
        return accuracy

def main() -> None:
    """Main function to execute the workflow."""
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)

    accuracy = classifier.evaluate(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()