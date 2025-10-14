"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-14T17:28:38.993549

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_and_prepare_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and split it into features and target variables.

    Returns:
        tuple: A tuple containing features (X) and target (y).
    """
    try:
        iris = load_iris()
        X = iris.data
        y = iris.target
        return X, y
    except Exception as e:
        logging.error("Error loading dataset: %s", e)
        raise

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        X (np.ndarray): Features data.
        y (np.ndarray): Target data.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        tuple: A tuple containing training features (X_train), testing features (X_test),
               training target (y_train), and testing target (y_test).
    """
    try:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    except Exception as e:
        logging.error("Error splitting data: %s", e)
        raise

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target.

    Returns:
        RandomForestClassifier: The trained classifier.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        logging.error("Error training model: %s", e)
        raise

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model and print accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained classifier.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing target.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info("Model Accuracy: %.2f%%", accuracy * 100)
        logging.info("Classification Report:\n%s", classification_report(y_test, y_pred))
    except Exception as e:
        logging.error("Error evaluating model: %s", e)
        raise

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    try:
        X, y = load_and_prepare_data()
        X_train, X_test, y_train, y_test = split_data(X, y)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        logging.error("An error occurred in the main workflow: %s", e)

if __name__ == "__main__":
    main()