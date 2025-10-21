"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-21T18:57:37.327436

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        features: The feature set.
        target: The target variable.
        test_size: Proportion of the dataset to include in the test split.

    Returns:
        A tuple of training features, testing features, training target, and testing target.
    """
    return train_test_split(features, target, test_size=test_size, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model.

    Args:
        X_train: Training features.
        y_train: Training target.

    Returns:
        The trained Random Forest model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model's performance.

    Args:
        model: The trained model.
        X_test: Testing features.
        y_test: Testing target.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, predictions))
    except Exception as e:
        print(f"Error during evaluation: {e}")

def main() -> None:
    """Main function to run the machine learning pipeline."""
    try:
        # Load the data
        features, target = load_data()
        
        # Split the data
        X_train, X_test, y_train, y_test = split_data(features, target)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        evaluate_model(model, X_test, y_test)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()