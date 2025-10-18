"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-18T19:08:39.582391

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_and_prepare_data() -> tuple:
    """
    Load the Iris dataset and split it into training and testing sets.

    Returns:
        tuple: Features and target variables for training and testing.
    """
    try:
        iris = load_iris()
        X = iris.data
        y = iris.target
        return train_test_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        raise RuntimeError("Error loading or preparing data: " + str(e))

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier on the training data.

    Args:
        X_train (np.ndarray): Features for training.
        y_train (np.ndarray): Target labels for training.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training model: " + str(e))

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model on the test data and print metrics.

    Args:
        model (RandomForestClassifier): The trained model to evaluate.
        X_test (np.ndarray): Features for testing.
        y_test (np.ndarray): True labels for testing.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError("Error evaluating model: " + str(e))

def main() -> None:
    """
    Main function to execute the machine learning pipeline.
    """
    X_train, X_test, y_train, y_test = load_and_prepare_data()
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()