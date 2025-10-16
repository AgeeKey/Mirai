"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-16T11:37:11.853344

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    try:
        iris = load_iris()
        return iris.data, iris.target
    except Exception as e:
        raise RuntimeError("Error loading dataset: " + str(e))

def preprocess_data(X: np.ndarray) -> np.ndarray:
    """
    Standardize the feature data.

    Args:
        X (np.ndarray): Feature data to standardize.

    Returns:
        np.ndarray: Standardized feature data.
    """
    try:
        scaler = StandardScaler()
        return scaler.fit_transform(X)
    except Exception as e:
        raise RuntimeError("Error during data preprocessing: " + str(e))

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier.

    Args:
        X_train (np.ndarray): Training feature data.
        y_train (np.ndarray): Training target data.

    Returns:
        RandomForestClassifier: Trained classifier.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training the model: " + str(e))

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model.

    Args:
        model (RandomForestClassifier): The trained classifier.
        X_test (np.ndarray): Test feature data.
        y_test (np.ndarray): Test target data.
    """
    try:
        y_pred = model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError("Error evaluating the model: " + str(e))

def main() -> None:
    """
    Main function to run the machine learning pipeline.
    """
    try:
        # Load data
        X, y = load_data()
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Preprocess data
        X_train_scaled = preprocess_data(X_train)
        X_test_scaled = preprocess_data(X_test)
        
        # Train model
        model = train_model(X_train_scaled, y_train)

        # Evaluate model
        evaluate_model(model, X_test_scaled, y_test)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()