"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T07:25:30.626495

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load dataset from a specified CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")
    return data

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """
    Preprocess the dataset to separate features and target variable.

    Args:
        data (pd.DataFrame): The input dataset.
        target_column (str): The name of the target column.

    Returns:
        tuple: Features (X) and target (y) as numpy arrays.
    """
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in data.")
    
    X = data.drop(columns=[target_column]).values
    y = data[target_column].values
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier model.

    Args:
        X (np.ndarray): Features.
        y (np.ndarray): Target variable.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model and print the classification report and confusion matrix.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): Test target variable.
    """
    y_pred = model.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

def main(file_path: str, target_column: str) -> None:
    """
    Main function to run the data pipeline.

    Args:
        file_path (str): The path to the CSV file.
        target_column (str): The name of the target column.
    """
    data = load_data(file_path)
    X, y = preprocess_data(data, target_column)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Example usage
    main("data.csv", "target_column_name")