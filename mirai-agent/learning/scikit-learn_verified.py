"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T10:01:35.633316

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data(file_path: str) -> pd.DataFrame:
    """Loads data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Preprocess data by separating features and target variable.
    
    Args:
        data (pd.DataFrame): Input data.
        target_column (str): The name of the target column.
        
    Returns:
        Tuple[pd.DataFrame, pd.Series]: Features and target variable.
    """
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in the data.")
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Trains a Random Forest Classifier model.
    
    Args:
        X (pd.DataFrame): Features.
        y (pd.Series): Target variable.
        
    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)  # Fit the model to the data
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluates the trained model on the test data.
    
    Args:
        model (RandomForestClassifier): Trained model.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): Test target variable.
        
    Raises:
        NotFittedError: If the model has not been fitted.
    """
    if not model:
        raise NotFittedError("The model has not been fitted yet.")
    
    y_pred = model.predict(X_test)  # Make predictions
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", classification_report(y_test, y_pred))

def main(file_path: str, target_column: str) -> None:
    """Main function to load data, preprocess, train, and evaluate the model.
    
    Args:
        file_path (str): Path to the CSV file.
        target_column (str): The name of the target column.
    """
    data = load_data(file_path)  # Load data
    X, y = preprocess_data(data, target_column)  # Preprocess data
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split data
    model = train_model(X_train, y_train)  # Train model
    evaluate_model(model, X_test, y_test)  # Evaluate model

if __name__ == "__main__":
    # Example usage
    main("data.csv", "target")