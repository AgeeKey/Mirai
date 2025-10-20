"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.78
Tests Passed: 0/1
Learned: 2025-10-20T09:45:36.387555

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and labels."""
    try:
        iris = load_iris()
        X = iris.data
        y = iris.target
        return X, y
    except Exception as e:
        logging.error("An error occurred while loading the data: %s", e)
        raise

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    try:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    except Exception as e:
        logging.error("An error occurred while splitting the data: %s", e)
        raise

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the training data."""
    try:
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        logging.error("An error occurred while training the model: %s", e)
        raise

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model and print the accuracy and classification report."""
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info("Model accuracy: %.2f%%", accuracy * 100)
        logging.info("Classification report:\n%s", classification_report(y_test, y_pred))
        logging.info("Confusion matrix:\n%s", confusion_matrix(y_test, y_pred))
    except Exception as e:
        logging.error("An error occurred while evaluating the model: %s", e)
        raise

def main() -> None:
    """Main function to execute the workflow."""
    try:
        X, y = load_data()
        X_train, X_test, y_train, y_test = split_data(X, y)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        logging.error("An error occurred in the main workflow: %s", e)

if __name__ == "__main__":
    main()