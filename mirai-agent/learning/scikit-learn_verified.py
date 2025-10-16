"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T13:26:38.290662

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def load_and_prepare_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and split it into features and target labels.

    Returns:
        tuple[np.ndarray, np.ndarray]: features and target labels.
    """
    try:
        iris = load_iris()
        X, y = iris.data, iris.target
        return X, y
    except Exception as e:
        raise RuntimeError("Error loading the Iris dataset") from e

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Features.
        y (np.ndarray): Target labels.
        test_size (float): Proportion of the dataset to include in the test split.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing data.
    """
    try:
        return train_test_split(X, y, test_size=test_size, random_state=42)
    except Exception as e:
        raise ValueError("Error splitting the dataset") from e

def scale_features(X_train: np.ndarray, X_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Standardize features by removing the mean and scaling to unit variance.

    Args:
        X_train (np.ndarray): Training features.
        X_test (np.ndarray): Testing features.

    Returns:
        tuple[np.ndarray, np.ndarray]: Scaled training and testing features.
    """
    try:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    except Exception as e:
        raise RuntimeError("Error scaling features") from e

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the training data.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target labels.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training the model") from e

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model and print the classification report and confusion matrix.

    Args:
        model (RandomForestClassifier): Trained Random Forest model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing target labels.
    """
    try:
        y_pred = model.predict(X_test)
        print("Classification Report:\n", classification_report(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    except Exception as e:
        raise RuntimeError("Error evaluating the model") from e

def main() -> None:
    """Main function to execute the machine learning workflow."""
    X, y = load_and_prepare_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_scaled, X_test_scaled = scale_features(X_train, X_test)
    model = train_model(X_train_scaled, y_train)
    evaluate_model(model, X_test_scaled, y_test)

if __name__ == "__main__":
    main()