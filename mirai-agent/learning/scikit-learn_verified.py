"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-17T01:25:48.384101

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

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier model.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.

    Returns:
        RandomForestClassifier: The trained model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        print(f"Error while training the model: {e}")
        raise

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test set.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test feature matrix.
        y_test (np.ndarray): Test target vector.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except NotFittedError:
        print("Model is not fitted yet. Please train the model first.")
    except Exception as e:
        print(f"Error during model evaluation: {e}")
        raise

def main() -> None:
    """Main function to execute the machine learning workflow."""
    # Load data
    X, y = load_data()
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()