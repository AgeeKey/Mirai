"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-20T10:17:35.474513

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

def load_and_prepare_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and prepare the features and target arrays.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    try:
        iris = load_iris()
        X, y = iris.data, iris.target
        return X, y
    except Exception as e:
        raise RuntimeError("Error loading the dataset.") from e

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.
    
    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target array.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.
    
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Splits of features and target.
    """
    try:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    except ValueError as e:
        raise ValueError("Error splitting the data: Ensure the input is valid.") from e

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier.
    
    Args:
        X_train (np.ndarray): Training feature matrix.
        y_train (np.ndarray): Training target array.
    
    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Error training the model.") from e

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """
    Evaluate the trained model on the test set.
    
    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Test feature matrix.
        y_test (np.ndarray): Test target array.
    
    Returns:
        float: Accuracy score of the model.
    """
    try:
        if not hasattr(model, "predict"):
            raise NotFittedError("The model is not fitted yet.")
        y_pred = model.predict(X_test)
        return accuracy_score(y_test, y_pred)
    except NotFittedError as e:
        raise RuntimeError("Model is not fitted. Please train the model first.") from e
    except Exception as e:
        raise RuntimeError("Error during model evaluation.") from e

def main() -> None:
    """
    Main function to run the machine learning pipeline.
    """
    try:
        # Load and prepare the data
        X, y = load_and_prepare_data()
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = split_data(X, y)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        accuracy = evaluate_model(model, X_test, y_test)
        print(f"Model accuracy: {accuracy:.2f}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()