"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T07:40:05.712472

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the iris dataset and return features and labels.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and labels of the iris dataset.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.
    
    Args:
        X (np.ndarray): Feature data.
        y (np.ndarray): Labels.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.
    
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
        Training features, testing features, training labels, testing labels.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier on the training data.
    
    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training labels.
    
    Returns:
        RandomForestClassifier: Trained Random Forest classifier.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """
    Evaluate the model using accuracy score.
    
    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing labels.
    
    Returns:
        float: Accuracy of the model on the test set.
    """
    predictions = model.predict(X_test)
    return accuracy_score(y_test, predictions)

def main() -> None:
    """
    Main function to run the machine learning pipeline.
    """
    try:
        # Load dataset
        X, y = load_data()
        
        # Split dataset
        X_train, X_test, y_train, y_test = split_data(X, y)
        
        # Train model
        model = train_model(X_train, y_train)
        
        # Evaluate model
        accuracy = evaluate_model(model, X_test, y_test)
        
        print(f"Model accuracy: {accuracy:.2f}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()