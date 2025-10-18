"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.75
Tests Passed: 0/1
Learned: 2025-10-18T10:49:25.523651

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
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError("Error loading dataset: " + str(e))

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    try:
        return train_test_split(features, target, test_size=test_size, random_state=42)
    except Exception as e:
        raise ValueError("Error splitting data: " + str(e))

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier."""
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training model: " + str(e))

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test set."""
    try:
        predictions = model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, predictions))
        print("Classification Report:\n", classification_report(y_test, predictions))
    except NotFittedError:
        print("Model is not fitted yet. Please train the model first.")
    except Exception as e:
        raise RuntimeError("Error during evaluation: " + str(e))

def main() -> None:
    """Main function to execute the workflow."""
    try:
        features, target = load_data()
        X_train, X_test, y_train, y_test = split_data(features, target)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print("An error occurred: " + str(e))

if __name__ == "__main__":
    main()