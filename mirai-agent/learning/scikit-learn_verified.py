"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-18T09:31:00.885231

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
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variable.
    """
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(features: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The input features.
        target (np.ndarray): The target labels.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
        Training features, testing features, training labels, testing labels.
    """
    return train_test_split(features, target, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model's performance.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing labels.
    """
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    print(f"Model Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    try:
        # Load data
        features, target = load_data()
        
        # Preprocess data
        X_train, X_test, y_train, y_test = preprocess_data(features, target)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        evaluate_model(model, X_test, y_test)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()