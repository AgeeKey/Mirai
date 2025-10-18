"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-18T22:17:11.860916

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

def split_data(features: np.ndarray, target: np.ndarray, test_size: float = 0.2) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets.
    
    Args:
        features: The feature data.
        target: The target labels.
        test_size: The proportion of the dataset to include in the test split.

    Returns:
        A tuple containing the training features, testing features, training labels, and testing labels.
    """
    return train_test_split(features, target, test_size=test_size, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier on the training data.
    
    Args:
        X_train: The training features.
        y_train: The training labels.

    Returns:
        A trained Random Forest classifier.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model using the test data.
    
    Args:
        model: The trained classifier.
        X_test: The test features.
        y_test: The test labels.
    """
    predictions = model.predict(X_test)
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

def main() -> None:
    """Main function to execute the machine learning workflow."""
    try:
        features, target = load_data()
        X_train, X_test, y_train, y_test = split_data(features, target)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()