"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-17T20:49:12.775312

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def load_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the data into training and testing sets.

    Args:
        features (np.ndarray): The features of the dataset.
        target (np.ndarray): The target labels of the dataset.
        test_size (float): The proportion of the dataset to include in the test split.

    Returns:
        tuple: Training features, test features, training labels, test labels.
    """
    try:
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_size, random_state=42)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        raise ValueError("Error in data splitting: " + str(e))

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the training data.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training labels.

    Returns:
        RandomForestClassifier: The trained classifier.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise ValueError("Error in model training: " + str(e))

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the results.

    Args:
        model (RandomForestClassifier): The trained classifier.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): Test labels.
    """
    try:
        y_pred = model.predict(X_test)
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
        print("\nClassification Report:\n", classification_report(y_test, y_pred))
    except Exception as e:
        raise ValueError("Error in model evaluation: " + str(e))

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    features, target = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(features, target)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()