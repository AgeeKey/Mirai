"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-15T13:21:43.129469

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
    """
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variable.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature data.
        y (np.ndarray): Target data.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Controls the randomness of the training and testing split.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training features, testing features, training target, testing target.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier.

    Args:
        X_train (np.ndarray): Training feature data.
        y_train (np.ndarray): Training target data.

    Returns:
        RandomForestClassifier: Trained classifier.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model on the test data.

    Args:
        model (RandomForestClassifier): Trained classifier.
        X_test (np.ndarray): Testing feature data.
        y_test (np.ndarray): Testing target data.

    Raises:
        NotFittedError: If the model has not been fitted before evaluation.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, predictions))
    except NotFittedError as e:
        print("Model has not been fitted yet. Please train the model before evaluation.")
        raise e

def main() -> None:
    """
    Main function to execute the workflow.
    """
    # Load data
    X, y = load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()