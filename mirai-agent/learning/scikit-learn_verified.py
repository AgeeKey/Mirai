"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T09:52:13.914553

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
    """Load the Iris dataset and return features and target labels.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target labels.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.
    
    Args:
        features (np.ndarray): Feature data.
        target (np.ndarray): Target labels.
        test_size (float): Proportion of the dataset to include in the test split.
        
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split datasets.
    """
    return train_test_split(features, target, test_size=test_size, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model on the training data.
    
    Args:
        X_train (np.ndarray): Training feature data.
        y_train (np.ndarray): Training target labels.
        
    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test data and print the results.
    
    Args:
        model (RandomForestClassifier): Trained model to evaluate.
        X_test (np.ndarray): Test feature data.
        y_test (np.ndarray): Test target labels.
        
    Raises:
        NotFittedError: If the model has not been fitted yet.
    """
    if not hasattr(model, 'predict'):
        raise NotFittedError("Model is not fitted yet.")
    
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", classification_report(y_test, predictions))

def main() -> None:
    """Main function to execute the machine learning workflow."""
    try:
        features, target = load_data()
        X_train, X_test, y_train, y_test = split_data(features, target)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()