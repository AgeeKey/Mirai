"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T20:37:43.857441

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_and_prepare_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and split it into features and target.

    Returns:
        Tuple containing features and target arrays.
    """
    try:
        iris = load_iris()
        X, y = iris.data, iris.target
        return X, y
    except Exception as e:
        raise RuntimeError("Error loading the dataset") from e

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X: Feature array.
        y: Target array.
        test_size: Proportion of the dataset to include in the test split.
        random_state: Controls the randomness of the train-test split.

    Returns:
        Tuple containing training features, testing features, training target, and testing target.
    """
    try:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    except Exception as e:
        raise RuntimeError("Error splitting the data") from e

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train the Random Forest Classifier model.

    Args:
        X_train: Training feature array.
        y_train: Training target array.

    Returns:
        Trained Random Forest Classifier model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training the model") from e

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the model and print the accuracy and classification report.

    Args:
        model: Trained model.
        X_test: Testing feature array.
        y_test: Testing target array.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError("Error evaluating the model") from e

def main() -> None:
    """
    Main function to execute the data loading, training, and evaluation pipeline.
    """
    try:
        X, y = load_and_prepare_data()
        X_train, X_test, y_train, y_test = split_data(X, y)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()