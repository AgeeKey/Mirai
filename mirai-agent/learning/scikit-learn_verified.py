"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-17T06:29:17.485185

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
    """Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variables.
    """
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature variables.
        y (np.ndarray): Target variable.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
        Training features, testing features, training labels, testing labels.
    """
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier.

    Args:
        X_train (np.ndarray): Training feature variables.
        y_train (np.ndarray): Training target variable.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """Evaluate the trained model on test data.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Test feature variables.
        y_test (np.ndarray): Test target variable.

    Returns:
        float: Accuracy of the model on the test set.
    """
    y_pred = model.predict(X_test)
    return accuracy_score(y_test, y_pred)

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    try:
        # Load data
        X, y = load_data()
        
        # Preprocess data
        X_train, X_test, y_train, y_test = preprocess_data(X, y)
        
        # Train model
        model = train_model(X_train, y_train)

        # Evaluate model
        accuracy = evaluate_model(model, X_test, y_test)
        print(f"Model accuracy: {accuracy:.2f}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()