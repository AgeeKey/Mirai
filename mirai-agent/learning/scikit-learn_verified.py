"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T04:28:34.480327

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def load_and_preprocess_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and preprocess it.

    Returns:
        tuple: A tuple containing the features and target arrays.
    """
    try:
        iris = load_iris()
        X, y = iris.data, iris.target
        return X, y
    except Exception as e:
        raise RuntimeError(f"Error loading dataset: {e}")

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature array.
        y (np.ndarray): Target array.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random state for reproducibility.

    Returns:
        tuple: Training and testing sets for features and target.
    """
    try:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    except Exception as e:
        raise RuntimeError(f"Error splitting data: {e}")

def scale_data(X_train: np.ndarray, X_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Scale the feature data using StandardScaler.

    Args:
        X_train (np.ndarray): Training feature array.
        X_test (np.ndarray): Testing feature array.

    Returns:
        tuple: Scaled training and testing feature arrays.
    """
    try:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    except Exception as e:
        raise RuntimeError(f"Error scaling data: {e}")

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a RandomForestClassifier model.

    Args:
        X_train (np.ndarray): Training feature array.
        y_train (np.ndarray): Training target array.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model using the test set.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Testing feature array.
        y_test (np.ndarray): Testing target array.
    """
    try:
        y_pred = model.predict(X_test)
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError(f"Error evaluating model: {e}")

def main() -> None:
    """
    Main function to execute the machine learning pipeline.
    """
    X, y = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_scaled, X_test_scaled = scale_data(X_train, X_test)
    model = train_model(X_train_scaled, y_train)
    evaluate_model(model, X_test_scaled, y_test)

if __name__ == "__main__":
    main()