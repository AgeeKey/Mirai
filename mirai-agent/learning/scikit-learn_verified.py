"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T13:15:59.775935

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.datasets import load_iris
from typing import Any, Dict, Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Loads the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    data = load_iris()
    return data.data, data.target

def preprocess_data(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Splits the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target array.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing feature and target sets.
    """
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        raise RuntimeError(f"Error during data splitting: {e}")

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Trains a Random Forest classifier on the training data.

    Args:
        X_train (np.ndarray): Training feature matrix.
        y_train (np.ndarray): Training target array.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError(f"Error during model training: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluates the model and prints the classification report and accuracy.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Testing feature matrix.
        y_test (np.ndarray): Testing target array.
    """
    try:
        y_pred = model.predict(X_test)
        print("Classification Report:\n", classification_report(y_test, y_pred))
        print("Accuracy:", accuracy_score(y_test, y_pred))
    except Exception as e:
        raise RuntimeError(f"Error during model evaluation: {e}")

def main() -> None:
    """Main function to execute the machine learning workflow."""
    X, y = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(X, y)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()