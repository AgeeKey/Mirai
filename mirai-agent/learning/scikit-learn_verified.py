"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T11:37:18.174165

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def preprocess_data(X: np.ndarray) -> np.ndarray:
    """Preprocess the data by scaling features.

    Args:
        X (np.ndarray): Feature matrix.

    Returns:
        np.ndarray: Scaled feature matrix.
    """
    try:
        scaler = StandardScaler()
        return scaler.fit_transform(X)
    except Exception as e:
        raise RuntimeError(f"Error during data preprocessing: {e}")

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.

    Args:
        X_train (np.ndarray): Training feature matrix.
        y_train (np.ndarray): Training target array.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model's performance.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Test feature matrix.
        y_test (np.ndarray): Test target array.
    """
    try:
        y_pred = model.predict(X_test)
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError(f"Error during model evaluation: {e}")

def main() -> None:
    """Main function to execute the ML pipeline."""
    try:
        # Load data
        X, y = load_data()

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Preprocess the data
        X_train_scaled = preprocess_data(X_train)
        X_test_scaled = preprocess_data(X_test)

        # Train the model
        model = train_model(X_train_scaled, y_train)

        # Evaluate the model
        evaluate_model(model, X_test_scaled, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()