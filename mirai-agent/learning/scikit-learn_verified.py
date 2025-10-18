"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T17:34:21.354716

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from typing import Tuple

def load_and_prepare_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and prepare features and labels.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and labels of the dataset.
    """
    try:
        iris = load_iris()
        X = iris.data
        y = iris.target
        return X, y
    except Exception as e:
        raise RuntimeError("Error loading the dataset: " + str(e))

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier on the provided data.

    Args:
        X (np.ndarray): Feature data.
        y (np.ndarray): Target labels.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        raise RuntimeError("Error training the model: " + str(e))

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model using accuracy and classification report.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Feature data for testing.
        y_test (np.ndarray): True labels for testing.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError("Error during model evaluation: " + str(e))

def main() -> None:
    """
    Main function to execute the workflow of loading data, training model, and evaluating it.
    """
    try:
        # Load and prepare data
        X, y = load_and_prepare_data()
        
        # Split dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = train_model(X_train, y_train)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print("An error occurred: ", str(e))

if __name__ == "__main__":
    main()