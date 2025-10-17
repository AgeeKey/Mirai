"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-17T10:31:30.096913

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load dataset from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> (pd.DataFrame, pd.Series):
    """
    Preprocess the data by separating features and target variable.

    Args:
        data (pd.DataFrame): Input dataframe.
        target_column (str): Name of the target variable column.

    Returns:
        (pd.DataFrame, pd.Series): Features and target variable.
    """
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in data.")

    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest classifier.

    Args:
        X (pd.DataFrame): Features for training.
        y (pd.Series): Target variable for training.

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
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): Test target variable.

    Returns:
        None
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main(file_path: str, target_column: str) -> None:
    """
    Main function to load data, preprocess, train and evaluate the model.

    Args:
        file_path (str): Path to the CSV file.
        target_column (str): Name of the target variable column.

    Returns:
        None
    """
    data = load_data(file_path)
    X, y = preprocess_data(data, target_column)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Replace 'data.csv' with your actual data file path and 'target' with your target column name.
    main('data.csv', 'target')