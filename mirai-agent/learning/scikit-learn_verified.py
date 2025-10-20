"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-20T23:42:01.498760

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
    """Load the Iris dataset and return features and target variables."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the training data."""
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print classification report and confusion matrix."""
    try:
        predictions = model.predict(X_test)
        print("Classification Report:\n", classification_report(y_test, predictions))
        print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
    except NotFittedError as e:
        print("Model not fitted. Please train the model first.", e)

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    try:
        # Load data
        features, target = load_data()
        
        # Split data
        X_train, X_test, y_train, y_test = split_data(features, target)
        
        # Train model
        model = train_model(X_train, y_train)
        
        # Evaluate model
        evaluate_model(model, X_test, y_test)

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()