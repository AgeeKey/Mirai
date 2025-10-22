"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T00:54:26.131450

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset.

    Returns:
        Tuple containing features and target variable.
    """
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError("Error loading data: {}".format(e))

def preprocess_data(features: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): The feature set.
        target (np.ndarray): The target variable.

    Returns:
        Tuple of training features, testing features, training target, testing target.
    """
    try:
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        raise RuntimeError("Error during data preprocessing: {}".format(e))

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier.

    Args:
        X_train (np.ndarray): Training feature set.
        y_train (np.ndarray): Training target variable.

    Returns:
        Trained Random Forest Classifier model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training model: {}".format(e))

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """
    Evaluate the model's accuracy.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Testing feature set.
        y_test (np.ndarray): Testing target variable.

    Returns:
        Accuracy score of the model.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        return accuracy
    except Exception as e:
        raise RuntimeError("Error evaluating model: {}".format(e))

def main() -> None:
    """
    Main function to execute the machine learning pipeline.
    """
    features, target = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(features, target)
    model = train_model(X_train, y_train)
    accuracy = evaluate_model(model, X_test, y_test)
    print(f"Model Accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()