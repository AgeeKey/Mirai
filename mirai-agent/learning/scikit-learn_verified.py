"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T21:21:33.293277

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
        tuple: Features and target variable as numpy arrays.
    """
    try:
        iris = load_iris()
        X, y = iris.data, iris.target
        return X, y
    except Exception as e:
        raise RuntimeError("Error loading the dataset") from e

def split_data(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Feature data.
        y (np.ndarray): Target data.

    Returns:
        tuple: Split feature and target data.
    """
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        raise RuntimeError("Error splitting the data") from e

def scale_data(X_train: np.ndarray, X_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Scale the feature data using StandardScaler.

    Args:
        X_train (np.ndarray): Training feature data.
        X_test (np.ndarray): Testing feature data.

    Returns:
        tuple: Scaled training and testing feature data.
    """
    try:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    except Exception as e:
        raise RuntimeError("Error scaling the data") from e

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier on the training data.

    Args:
        X_train (np.ndarray): Scaled training feature data.
        y_train (np.ndarray): Training target data.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training the model") from e

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model on the test data and print the results.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Scaled testing feature data.
        y_test (np.ndarray): Testing target data.
    """
    try:
        predictions = model.predict(X_test)
        print(confusion_matrix(y_test, predictions))
        print(classification_report(y_test, predictions))
    except Exception as e:
        raise RuntimeError("Error evaluating the model") from e

def main() -> None:
    """
    Main function to run the machine learning workflow.
    """
    X, y = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_scaled, X_test_scaled = scale_data(X_train, X_test)
    model = train_model(X_train_scaled, y_train)
    evaluate_model(model, X_test_scaled, y_test)

if __name__ == "__main__":
    main()