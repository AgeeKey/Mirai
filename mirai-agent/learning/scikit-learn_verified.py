"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-21T06:33:56.352846

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset."""
    iris = load_iris()
    return iris.data, iris.target

def split_data(data: np.ndarray, target: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    try:
        return train_test_split(data, target, test_size=test_size, random_state=random_state)
    except Exception as e:
        raise ValueError(f"Error occurred while splitting data: {e}")

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier."""
    model = RandomForestClassifier(random_state=42)
    try:
        model.fit(X_train, y_train)
    except Exception as e:
        raise ValueError(f"Error occurred while training the model: {e}")
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """Evaluate the model's accuracy."""
    try:
        predictions = model.predict(X_test)
        return accuracy_score(y_test, predictions)
    except NotFittedError:
        raise RuntimeError("Model is not fitted yet.")
    except Exception as e:
        raise ValueError(f"Error occurred during model evaluation: {e}")

def main() -> None:
    """Main function to run the machine learning pipeline."""
    data, target = load_data()
    X_train, X_test, y_train, y_test = split_data(data, target)
    model = train_model(X_train, y_train)
    accuracy = evaluate_model(model, X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()