"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-20T14:36:05.260671

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from typing import Any

def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """Preprocess the data by splitting into features and target, and scaling features.

    Args:
        data (pd.DataFrame): The dataset.
        target_column (str): The name of the target column.

    Returns:
        tuple: Features (X) and target (y) as separate arrays.
    """
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier model.

    Args:
        X (np.ndarray): Feature set.
        y (np.ndarray): Target variable.

    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X: np.ndarray, y: np.ndarray) -> None:
    """Evaluate the trained model using confusion matrix and classification report.

    Args:
        model (RandomForestClassifier): The trained model.
        X (np.ndarray): Feature set.
        y (np.ndarray): Target variable.
    """
    y_pred = model.predict(X)
    print("Confusion Matrix:")
    print(confusion_matrix(y, y_pred))
    print("\nClassification Report:")
    print(classification_report(y, y_pred))

def main(file_path: str, target_column: str) -> None:
    """Main function to load data, preprocess it, train the model, and evaluate it.

    Args:
        file_path (str): The path to the CSV file.
        target_column (str): The name of the target column.
    """
    data = load_data(file_path)
    X, y = preprocess_data(data, target_column)
    
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Replace 'your_dataset.csv' with the path to your dataset and 'target' with the target column name
    main('your_dataset.csv', 'target')