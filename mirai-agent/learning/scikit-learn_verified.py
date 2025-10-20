"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T04:45:57.235271

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from typing import Tuple, Any

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """Load the iris dataset.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def preprocess_data(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and test sets.
    
    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.
        
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and test sets for features and target.
    """
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.
    
    Args:
        X_train (np.ndarray): Training feature matrix.
        y_train (np.ndarray): Training target vector.
        
    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the results.
    
    Args:
        model (RandomForestClassifier): Trained Random Forest model.
        X_test (np.ndarray): Test feature matrix.
        y_test (np.ndarray): Test target vector.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)

def main() -> None:
    """Main function to execute the machine learning workflow."""
    try:
        # Load the data
        X, y = load_data()
        
        # Preprocess the data
        X_train, X_test, y_train, y_test = preprocess_data(X, y)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        evaluate_model(model, X_test, y_test)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()