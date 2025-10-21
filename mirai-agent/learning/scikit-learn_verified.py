"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-21T15:58:48.831685

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file.
    
    Args:
        file_path (str): The path to the CSV file.
    
    Returns:
        pd.DataFrame: The loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """Preprocess the data by separating features and target, then scaling features.
    
    Args:
        data (pd.DataFrame): The input data.
        target_column (str): The name of the target column.
    
    Returns:
        tuple: A tuple containing the scaled features and the target variable.
    """
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

def train_model(X: np.ndarray, y: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest model on the provided data.
    
    Args:
        X (np.ndarray): The feature data.
        y (pd.Series): The target variable.
    
    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: pd.Series) -> None:
    """Evaluate the model's performance on the test set.
    
    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): The test feature data.
        y_test (pd.Series): The test target variable.
    """
    y_pred = model.predict(X_test)
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

def main(file_path: str, target_column: str) -> None:
    """Main function to load data, preprocess it, train and evaluate the model.
    
    Args:
        file_path (str): The path to the CSV file.
        target_column (str): The name of the target column.
    """
    data = load_data(file_path)
    X, y = preprocess_data(data, target_column)
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Example usage, replace with your own file path and target column name
    main("path/to/your/data.csv", "target_column_name")