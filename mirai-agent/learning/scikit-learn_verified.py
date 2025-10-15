"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T23:40:13.908839

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from typing import Tuple

def load_and_prepare_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and split it into features and target labels.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    try:
        iris = load_iris()
        X = iris.data
        y = iris.target
        return X, y
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.
    
    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target array.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split feature and target arrays.
    """
    try:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    except Exception as e:
        raise ValueError(f"Error splitting data: {e}")

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier on the training data.
    
    Args:
        X_train (np.ndarray): Training feature matrix.
        y_train (np.ndarray): Training target array.
    
    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model on the testing data and print metrics.
    
    Args:
        model (RandomForestClassifier): Trained model to evaluate.
        X_test (np.ndarray): Testing feature matrix.
        y_test (np.ndarray): Testing target array.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    except Exception as e:
        raise RuntimeError(f"Error evaluating model: {e}")

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    X, y = load_and_prepare_data()  # Load data
    X_train, X_test, y_train, y_test = split_data(X, y)  # Split data
    model = train_model(X_train, y_train)  # Train model
    evaluate_model(model, X_test, y_test)  # Evaluate model

if __name__ == "__main__":
    main()  # Run the main function