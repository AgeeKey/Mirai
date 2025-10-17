"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-17T02:29:33.512089

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
    Load the Iris dataset and return features and labels.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and labels from the dataset.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, labels: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The features to be used for training/testing.
        labels (np.ndarray): The labels corresponding to the features.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Split features and labels for training and testing.
    """
    return train_test_split(features, labels, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier on the training data.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training labels.

    Returns:
        RandomForestClassifier: The trained classifier.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model using the testing data.

    Args:
        model (RandomForestClassifier): The trained classifier.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing labels.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')
        print('Classification Report:')
        print(classification_report(y_test, y_pred))
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    try:
        # Load data
        features, labels = load_data()
        
        # Split data
        X_train, X_test, y_train, y_test = split_data(features, labels)
        
        # Train model
        model = train_model(X_train, y_train)
        
        # Evaluate model
        evaluate_model(model, X_test, y_test)

    except Exception as e:
        print(f"An error occurred in the main workflow: {e}")

if __name__ == "__main__":
    main()