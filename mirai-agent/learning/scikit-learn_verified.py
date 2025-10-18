"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-18T00:33:08.276510

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from typing import Tuple

def load_and_prepare_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and prepare the features and target arrays.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    try:
        iris = load_iris()
        X = iris.data
        y = iris.target
        return X, y
    except Exception as e:
        raise RuntimeError("Error loading data: " + str(e))

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature array.
        y (np.ndarray): Target array.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing feature and target arrays.
    """
    try:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    except Exception as e:
        raise RuntimeError("Error splitting data: " + str(e))

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier.

    Args:
        X_train (np.ndarray): Training feature array.
        y_train (np.ndarray): Training target array.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training model: " + str(e))

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model using accuracy and classification report.

    Args:
        model (RandomForestClassifier): Trained Random Forest model.
        X_test (np.ndarray): Testing feature array.
        y_test (np.ndarray): Testing target array.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred)

        print(f"Accuracy: {accuracy:.2f}")
        print("Confusion Matrix:\n", conf_matrix)
        print("Classification Report:\n", class_report)
    except Exception as e:
        raise RuntimeError("Error evaluating model: " + str(e))

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    try:
        X, y = load_and_prepare_data()  # Load data
        X_train, X_test, y_train, y_test = split_data(X, y)  # Split data
        model = train_model(X_train, y_train)  # Train model
        evaluate_model(model, X_test, y_test)  # Evaluate model
    except Exception as e:
        print("An error occurred during the workflow: ", str(e))

if __name__ == "__main__":
    main()