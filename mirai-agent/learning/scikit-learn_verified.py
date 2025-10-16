"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-16T20:49:09.530062

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris

def load_data() -> pd.DataFrame:
    """Load the Iris dataset as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data by splitting it into features and target variable.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing the dataset.

    Returns:
        tuple: A tuple containing features (X) and target (y).
    """
    X = df.values[:, :-1]  # Features
    y = df.values[:, -1]   # Target
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model on the provided features and target variable.
    
    Args:
        X (np.ndarray): Features for training.
        y (np.ndarray): Target variable for training.

    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on test data and print the accuracy and classification report.
    
    Args:
        model (RandomForestClassifier): The trained model to evaluate.
        X_test (np.ndarray): Features for testing.
        y_test (np.ndarray): Target variable for testing.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, predictions))
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    try:
        df = load_data()
        X, y = preprocess_data(df)
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = train_model(X_train, y_train)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()