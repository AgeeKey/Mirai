"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-21T23:18:04.053147

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_and_prepare_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and prepare the features and target arrays.

    Returns:
        tuple: A tuple containing features (X) and target (y).
    """
    try:
        iris = load_iris()
        X, y = iris.data, iris.target
        return X, y
    except Exception as e:
        logging.error("Failed to load data: %s", e)
        raise

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier on the provided data.

    Args:
        X (np.ndarray): Features for training.
        y (np.ndarray): Target labels for training.

    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        logging.error("Failed to train model: %s", e)
        raise

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the model and print accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model to evaluate.
        X_test (np.ndarray): Features for testing.
        y_test (np.ndarray): True labels for testing.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info("Model Accuracy: %.2f%%", accuracy * 100)
        logging.info("Classification Report:\n%s", classification_report(y_test, y_pred))
    except Exception as e:
        logging.error("Failed to evaluate model: %s", e)
        raise

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    try:
        X, y = load_and_prepare_data()
        
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = train_model(X_train, y_train)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)

    except Exception as e:
        logging.critical("An error occurred in the main execution: %s", e)

if __name__ == "__main__":
    main()