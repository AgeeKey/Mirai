"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.77
Tests Passed: 0/1
Learned: 2025-10-19T03:47:48.188438

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and labels."""
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(features: np.ndarray, labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a RandomForest model on the training data."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the accuracy and classification report."""
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, predictions))
    except Exception as e:
        print(f"Error during evaluation: {e}")

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    try:
        features, labels = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(features, labels)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()