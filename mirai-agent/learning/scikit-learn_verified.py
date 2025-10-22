"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 1/1
Learned: 2025-10-22T18:29:39.237176

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
    """
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variables.
    """
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError("Error loading data: " + str(e))

def preprocess_data(features: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The input features.
        target (np.ndarray): The target variable.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training features, testing features, training target, testing target.
    """
    try:
        return train_test_split(features, target, test_size=0.2, random_state=42)
    except Exception as e:
        raise RuntimeError("Error during data preprocessing: " + str(e))

class IrisClassifier:
    def __init__(self):
        """
        Initialize the IrisClassifier with a Random Forest model.
        """
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the Random Forest model.

        Args:
            X_train (np.ndarray): The training features.
            y_train (np.ndarray): The training target.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise RuntimeError("Error training the model: " + str(e))

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the target for the test set.

        Args:
            X_test (np.ndarray): The testing features.

        Returns:
            np.ndarray: The predicted target.
        """
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            raise RuntimeError("The model has not been trained yet.")
        except Exception as e:
            raise RuntimeError("Error during prediction: " + str(e))

def main() -> None:
    """
    Main function to execute the workflow.
    """
    features, target = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(features, target)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)

    predictions = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("Accuracy:", accuracy)
    print("Classification Report:\n", classification_report(y_test, predictions))

if __name__ == "__main__":
    main()