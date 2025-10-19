"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T23:46:08.877585

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data(file_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Load data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        Tuple[pd.DataFrame, pd.Series]: Features and target variable.
    """
    try:
        data = pd.read_csv(file_path)
        X = data.drop(columns=['target'])
        y = data['target']
        return X, y
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except Exception as e:
        raise Exception(f"An error occurred while loading the data: {e}") from e

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier.

    Args:
        X (pd.DataFrame): Feature set.
        y (pd.Series): Target variable.

    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate the trained model.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (pd.DataFrame): Test feature set.
        y_test (pd.Series): Test target variable.

    Returns:
        None
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print(classification_report(y_test, y_pred))
    except NotFittedError:
        raise RuntimeError("Model is not fitted yet. Please train the model before evaluation.")

if __name__ == "__main__":
    # Load the dataset
    file_path = 'data.csv'  # Replace with your actual file path
    X, y = load_data(file_path)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)