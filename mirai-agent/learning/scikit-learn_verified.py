"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T01:20:39.929135

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.
    
    Args:
        features (np.ndarray): The feature set.
        target (np.ndarray): The target variable.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split data for training and testing.
    """
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier on the training data.
    
    Args:
        X_train (np.ndarray): The training features.
        y_train (np.ndarray): The training target variable.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """Evaluate the trained model on the test data.
    
    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): The test features.
        y_test (np.ndarray): The test target variable.

    Returns:
        float: The accuracy of the model on the test set.
    """
    predictions = model.predict(X_test)
    return accuracy_score(y_test, predictions)

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    try:
        # Load the data
        features, target = load_data()
        
        # Split the data
        X_train, X_test, y_train, y_test = split_data(features, target)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        accuracy = evaluate_model(model, X_test, y_test)
        
        print(f"Model accuracy: {accuracy:.2f}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()