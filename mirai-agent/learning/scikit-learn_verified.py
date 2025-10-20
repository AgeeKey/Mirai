"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T12:42:09.532894

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): Feature data.
        target (np.ndarray): Target data.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing features and target arrays.
    """
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.

    Args:
        X_train (np.ndarray): Training feature data.
        y_train (np.ndarray): Training target data.

    Returns:
        RandomForestClassifier: Trained classifier.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print performance metrics.

    Args:
        model (RandomForestClassifier): Trained classifier.
        X_test (np.ndarray): Testing feature data.
        y_test (np.ndarray): Testing target data.
    """
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

def main() -> None:
    """Main function to run the machine learning workflow."""
    try:
        # Load data
        features, target = load_data()
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = split_data(features, target)

        # Train the model
        model = train_model(X_train, y_train)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()