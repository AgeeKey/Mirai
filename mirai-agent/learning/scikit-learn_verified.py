"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-19T23:30:25.142225

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the iris dataset and return features and target."""
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    try:
        return train_test_split(features, target, test_size=test_size, random_state=42)
    except Exception as e:
        raise ValueError(f"Error splitting data: {e}")

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model."""
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the classification report and accuracy."""
    try:
        y_pred = model.predict(X_test)
        print(classification_report(y_test, y_pred))
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    except Exception as e:
        raise RuntimeError(f"Error evaluating model: {e}")

def main() -> None:
    """Main function to run the machine learning pipeline."""
    features, target = load_data()  # Load data
    X_train, X_test, y_train, y_test = split_data(features, target)  # Split data
    model = train_model(X_train, y_train)  # Train model
    evaluate_model(model, X_test, y_test)  # Evaluate model

if __name__ == "__main__":
    main()  # Execute the main function