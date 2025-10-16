"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-16T14:02:47.893376

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
    """Load the Iris dataset and return features and labels."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, labels: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The feature data.
        labels (np.ndarray): The target labels.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split data (X_train, X_test, y_train, y_test).
    """
    return train_test_split(features, labels, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier on the training data.

    Args:
        X_train (np.ndarray): The training feature data.
        y_train (np.ndarray): The training labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test data.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): The test feature data.
        y_test (np.ndarray): The test labels.
    """
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, predictions))

def main() -> None:
    """Main function to execute the machine learning workflow."""
    try:
        # Load data
        features, labels = load_data()
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = split_data(features, labels)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        evaluate_model(model, X_test, y_test)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()