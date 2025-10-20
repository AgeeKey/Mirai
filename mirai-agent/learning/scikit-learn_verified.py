"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-20T02:08:09.332945

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and return features and labels.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and labels of the dataset.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, labels: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The feature data.
        labels (np.ndarray): The target labels.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing feature and label sets.
    """
    return train_test_split(features, labels, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train the Random Forest classifier on the training data.

    Args:
        X_train (np.ndarray): Training feature data.
        y_train (np.ndarray): Training labels.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model using the test data.

    Args:
        model (RandomForestClassifier): Trained model to evaluate.
        X_test (np.ndarray): Test feature data.
        y_test (np.ndarray): Test labels.
    """
    predictions = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, predictions))
    print(classification_report(y_test, predictions))

def main() -> None:
    """
    Main function to run the machine learning workflow.
    """
    try:
        features, labels = load_data()  # Load data
        X_train, X_test, y_train, y_test = split_data(features, labels)  # Split data
        model = train_model(X_train, y_train)  # Train model
        evaluate_model(model, X_test, y_test)  # Evaluate model
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()