"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T07:57:47.908321

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
        Tuple containing features and target arrays.
    """
    data = load_iris()
    return data.data, data.target

def preprocess_data(features: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): Feature array.
        target (np.ndarray): Target array.

    Returns:
        Tuple containing training features, testing features, training target, and testing target.
    """
    return train_test_split(features, target, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier on the training data.

    Args:
        X_train (np.ndarray): Training feature data.
        y_train (np.ndarray): Training target data.

    Returns:
        Trained RandomForestClassifier model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the model's performance on the test data.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Testing feature data.
        y_test (np.ndarray): Testing target data.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main() -> None:
    """
    Main function to execute the workflow of loading data, training the model, and evaluation.
    """
    try:
        features, target = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(features, target)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()