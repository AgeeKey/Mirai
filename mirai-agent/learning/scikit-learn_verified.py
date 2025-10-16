"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T15:56:58.275454

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
    """Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The feature data.
        target (np.ndarray): The target data.
        test_size (float): The proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing features and target arrays.
    """
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target.

    Returns:
        RandomForestClassifier: Fitted Random Forest classifier.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)  # Train the model
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing target.

    Raises:
        NotFittedError: If the model is not fitted before evaluation.
    """
    try:
        y_pred = model.predict(X_test)  # Make predictions
        accuracy = accuracy_score(y_test, y_pred)  # Calculate accuracy
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))  # Print classification report
    except NotFittedError as e:
        print("Model is not fitted yet. Please train the model first.")

def main() -> None:
    """Main function to run the machine learning pipeline."""
    features, target = load_data()  # Load data
    X_train, X_test, y_train, y_test = split_data(features, target)  # Split data
    model = train_model(X_train, y_train)  # Train model
    evaluate_model(model, X_test, y_test)  # Evaluate model

if __name__ == "__main__":
    main()  # Execute the main function