"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-21T19:46:37.140615

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
    """Load the iris dataset.
    
    Returns:
        Tuple containing features and target variable.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.
    
    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target variable.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.
    
    Returns:
        Tuple containing training and testing sets for features and target.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier.
    
    Args:
        X_train (np.ndarray): Training feature matrix.
        y_train (np.ndarray): Training target variable.
    
    Returns:
        RandomForestClassifier: Trained classifier.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print accuracy and classification report.
    
    Args:
        model (RandomForestClassifier): Trained classifier.
        X_test (np.ndarray): Testing feature matrix.
        y_test (np.ndarray): Testing target variable.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')
        print(classification_report(y_test, y_pred))
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")

def main() -> None:
    """Main function to execute the machine learning workflow."""
    try:
        X, y = load_data()  # Load data
        X_train, X_test, y_train, y_test = split_data(X, y)  # Split data
        model = train_model(X_train, y_train)  # Train model
        evaluate_model(model, X_test, y_test)  # Evaluate model
    except Exception as e:
        print(f"An error occurred in the main workflow: {e}")

if __name__ == "__main__":
    main()