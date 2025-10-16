"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-16T06:37:05.341419

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the iris dataset and return features and target.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError(f"Failed to load data: {e}")

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a RandomForestClassifier on the provided data.
    
    Args:
        X (np.ndarray): Feature data.
        y (np.ndarray): Target data.
    
    Returns:
        RandomForestClassifier: Trained classifier.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        raise RuntimeError(f"Model training failed: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the accuracy and classification report.
    
    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test feature data.
        y_test (np.ndarray): Test target data.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, predictions))
    except Exception as e:
        raise RuntimeError(f"Model evaluation failed: {e}")

def main() -> None:
    """Main function to execute the workflow of loading data, training, and evaluating a model."""
    # Load dataset
    X, y = load_data()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()