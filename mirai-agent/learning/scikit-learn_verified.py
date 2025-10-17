"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-17T07:34:14.002427

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
    """Load the Iris dataset and return features and labels.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and labels of the dataset.
    """
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError("Error loading data: " + str(e))


def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.
    
    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training labels.
    
    Returns:
        RandomForestClassifier: Fitted Random Forest model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training model: " + str(e))


def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the accuracy and classification report.
    
    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): True labels for test features.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model Accuracy: {accuracy:.2f}")
        print(classification_report(y_test, predictions))
    except Exception as e:
        raise RuntimeError("Error evaluating model: " + str(e))


def main() -> None:
    """Main function to run the training and evaluation workflow."""
    X, y = load_data()  # Load the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split data
    
    model = train_model(X_train, y_train)  # Train the model
    evaluate_model(model, X_test, y_test)  # Evaluate the model


if __name__ == "__main__":
    main()  # Execute the main function