"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-21T20:52:07.958586

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def preprocess_data(df: pd.DataFrame, target_column: str) -> tuple:
    """
    Preprocess the data by separating features and target variable.

    Args:
        df (pd.DataFrame): The input DataFrame.
        target_column (str): The name of the target column.

    Returns:
        tuple: A tuple containing features (X) and target (y).
    """
    if target_column not in df.columns:
        raise ValueError("Target column not found in DataFrame")

    X = df.drop(columns=[target_column])
    y = df[target_column]
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest model.

    Args:
        X (pd.DataFrame): Features for training.
        y (pd.Series): Target variable for training.

    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate the model and print the accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (pd.DataFrame): Features for testing.
        y_test (pd.Series): True labels for testing.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main(file_path: str, target_column: str) -> None:
    """
    Main function to load data, preprocess it, train the model, and evaluate it.

    Args:
        file_path (str): The path to the CSV data file.
        target_column (str): The name of the target column.
    """
    # Load data
    data = load_data(file_path)

    # Preprocess data
    X, y = preprocess_data(data, target_column)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Example usage
    main('data.csv', 'target_column_name')