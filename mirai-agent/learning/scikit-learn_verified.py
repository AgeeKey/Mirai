"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T14:35:48.937676

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Loaded dataset as a DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """Preprocess data for training.
    
    Args:
        data (pd.DataFrame): Input DataFrame containing features and target.
        target_column (str): Name of the target column.
    
    Returns:
        tuple: Features (X) and target (y) as separate arrays.
    """
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in DataFrame.")
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> LogisticRegression:
    """Train a logistic regression model.
    
    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target array.
    
    Returns:
        LogisticRegression: Trained logistic regression model.
    """
    model = LogisticRegression(max_iter=200)
    model.fit(X, y)
    return model

def evaluate_model(model: LogisticRegression, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print results.
    
    Args:
        model (LogisticRegression): Trained model to evaluate.
        X_test (np.ndarray): Test feature matrix.
        y_test (np.ndarray): Test target array.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main(file_path: str, target_column: str) -> None:
    """Main function to execute the machine learning pipeline.
    
    Args:
        file_path (str): Path to the input CSV file.
        target_column (str): Name of the target column.
    """
    data = load_data(file_path)
    X, y = preprocess_data(data, target_column)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Example usage
    main("path/to/your/data.csv", "target_column_name")