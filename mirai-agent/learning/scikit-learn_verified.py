"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T05:17:36.134343

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variable.
    """
    iris = load_iris()
    return iris.data, iris.target

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier.

    Args:
        X (np.ndarray): Feature dataset.
        y (np.ndarray): Target variable.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """
    Evaluate the trained model using accuracy score.

    Args:
        model (RandomForestClassifier): Trained Random Forest model.
        X_test (np.ndarray): Test feature dataset.
        y_test (np.ndarray): Test target variable.

    Returns:
        float: Accuracy of the model on the test dataset.
    """
    try:
        predictions = model.predict(X_test)
    except NotFittedError as e:
        raise RuntimeError("Model must be fitted before evaluation.") from e

    accuracy = accuracy_score(y_test, predictions)
    return accuracy

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    # Load the dataset
    X, y = load_data()
    
    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    accuracy = evaluate_model(model, X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()