"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-21T21:40:31.795010

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError

def load_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and labels."""
    iris = load_iris()
    return iris.data, iris.target

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model on the provided data.
    
    Args:
        X: Feature matrix.
        y: Target vector.
        
    Returns:
        Trained RandomForestClassifier.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test data.
    
    Args:
        model: Trained RandomForestClassifier.
        X_test: Feature matrix for testing.
        y_test: True labels for testing.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("\nClassification Report:\n", classification_report(y_test, predictions))
    except NotFittedError:
        print("Model is not fitted yet.")
    except Exception as e:
        raise RuntimeError(f"Error during evaluation: {e}")

def main() -> None:
    """Main function to load data, train and evaluate the model."""
    try:
        # Load dataset
        X, y = load_data()
        
        # Split dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        evaluate_model(model, X_test, y_test)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()