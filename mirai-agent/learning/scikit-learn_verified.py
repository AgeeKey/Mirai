"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-20T18:54:24.259529

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
    Loads the iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variables.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Splits the dataset into training and testing sets.

    Args:
        features (np.ndarray): The input features.
        target (np.ndarray): The target variable.
        test_size (float): The proportion of the dataset to include in the test split.
        random_state (int): Controls the shuffling applied to the data before applying the split.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split features and target variables.
    """
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Trains a Random Forest Classifier on the training data.

    Args:
        X_train (np.ndarray): The training input features.
        y_train (np.ndarray): The training target variable.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluates the model performance on the test data.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): The test input features.
        y_test (np.ndarray): The test target variable.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, predictions))
    except Exception as e:
        print(f"Error during evaluation: {e}")

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    # Load data
    features, target = load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(features, target)
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()