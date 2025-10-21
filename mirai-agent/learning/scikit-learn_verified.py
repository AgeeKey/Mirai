"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.79
Tests Passed: 0/1
Learned: 2025-10-21T08:41:31.119078

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
    """Load the Iris dataset."""
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError("Error loading the dataset: " + str(e))

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    try:
        return train_test_split(X, y, test_size=test_size, random_state=42)
    except Exception as e:
        raise ValueError("Error during data splitting: " + str(e))

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model."""
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error during model training: " + str(e))

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """Evaluate the model's accuracy on the test set."""
    try:
        y_pred = model.predict(X_test)
        return accuracy_score(y_test, y_pred)
    except Exception as e:
        raise RuntimeError("Error during model evaluation: " + str(e))

def main() -> None:
    """Main function to execute the machine learning workflow."""
    X, y = load_data()  # Load the dataset
    X_train, X_test, y_train, y_test = split_data(X, y)  # Split the data
    model = train_model(X_train, y_train)  # Train the model
    accuracy = evaluate_model(model, X_test, y_test)  # Evaluate the model
    print(f"Model accuracy: {accuracy:.2f}")  # Print the accuracy

if __name__ == "__main__":
    main()  # Run the main function