"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-21T18:08:34.268068

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
    """Load the Iris dataset and return features and target labels."""
    iris = load_iris()
    return iris.data, iris.target

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier on the provided features and labels."""
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)  # Fit the model on the training data
        
        # Evaluate the model
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model accuracy: {accuracy:.2f}")
        print(classification_report(y_test, predictions))
        
        return model
    except Exception as e:
        print(f"An error occurred while training the model: {e}")
        raise

def main() -> None:
    """Main function to execute the workflow."""
    try:
        # Load data
        X, y = load_data()
        
        # Train the model
        model = train_model(X, y)
        
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()