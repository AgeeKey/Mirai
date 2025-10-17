"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-17T14:51:29.619573

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
    """
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target array.
    """
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def preprocess_data(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Train and test sets.
    """
    try:
        return train_test_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        raise RuntimeError(f"Error during data splitting: {e}")

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier.

    Args:
        X_train (np.ndarray): Training feature matrix.
        y_train (np.ndarray): Training target vector.

    Returns:
        RandomForestClassifier: Trained classifier.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError(f"Error during model training: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test feature matrix.
        y_test (np.ndarray): Test target vector.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)
    except Exception as e:
        raise RuntimeError(f"Error during model evaluation: {e}")

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    try:
        X, y = load_data()  # Load the dataset
        X_train, X_test, y_train, y_test = preprocess_data(X, y)  # Preprocess the data
        model = train_model(X_train, y_train)  # Train the model
        evaluate_model(model, X_test, y_test)  # Evaluate the model
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()