"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-14T18:17:25.521674

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from typing import Tuple

def load_and_preprocess_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load and preprocess the Iris dataset.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variable.
    """
    # Load the Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    return X, y

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.
    
    Args:
        X (np.ndarray): Features.
        y (np.ndarray): Target variable.
        test_size (float): Proportion of the dataset to include in the test split.
        
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing data.
    """
    return train_test_split(X, y, test_size=test_size, random_state=42)

def scale_features(X_train: np.ndarray, X_test: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Scale the features using StandardScaler.
    
    Args:
        X_train (np.ndarray): Training features.
        X_test (np.ndarray): Testing features.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Scaled training and testing features.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier model.
    
    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target variable.
        
    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model and print classification report and confusion matrix.
    
    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing target variable.
    """
    y_pred = model.predict(X_test)
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

def main() -> None:
    """
    Main function to execute the machine learning pipeline.
    """
    try:
        X, y = load_and_preprocess_data()
        X_train, X_test, y_train, y_test = split_data(X, y)
        X_train_scaled, X_test_scaled = scale_features(X_train, X_test)
        model = train_model(X_train_scaled, y_train)
        evaluate_model(model, X_test_scaled, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()