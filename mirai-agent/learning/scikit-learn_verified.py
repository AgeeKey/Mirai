"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.79
Tests Passed: 0/1
Learned: 2025-10-21T09:29:42.388609

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
    """Load the iris dataset and return features and target arrays."""
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError("Failed to load data") from e

def split_data(features: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    try:
        return train_test_split(features, target, test_size=0.2, random_state=42)
    except Exception as e:
        raise RuntimeError("Failed to split data") from e

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier."""
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Failed to train model") from e

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the accuracy and classification report."""
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
    except NotFittedError:
        print("Model has not been fitted yet!")
    except Exception as e:
        raise RuntimeError("Failed to evaluate model") from e

def main() -> None:
    """Main function to execute the data loading, training, and evaluation."""
    features, target = load_data()  # Load the dataset
    X_train, X_test, y_train, y_test = split_data(features, target)  # Split the data
    model = train_model(X_train, y_train)  # Train the model
    evaluate_model(model, X_test, y_test)  # Evaluate the model

if __name__ == "__main__":
    main()  # Run the main function