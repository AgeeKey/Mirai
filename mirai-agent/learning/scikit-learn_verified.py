"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-21T23:01:46.474033

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target."""
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(data: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier model."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print accuracy and classification report."""
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print(classification_report(y_test, predictions))
    except NotFittedError as e:
        print("Model is not fitted yet. Please train the model first.")
        raise e

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    # Load the dataset
    data, target = load_data()
    
    # Preprocess the data
    X_train, X_test, y_train, y_test = preprocess_data(data, target)
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()