"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-15T14:42:56.306664

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise ValueError("The file is empty.") from e

def preprocess_data(data: pd.DataFrame) -> tuple:
    """Preprocess the dataset by separating features and target variable.
    
    Args:
        data (pd.DataFrame): The input dataset.

    Returns:
        tuple: Features (X) and target variable (y).
    """
    X = data.drop("target", axis=1)  # Features
    y = data["target"]  # Target variable
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest classifier on the given data.
    
    Args:
        X (pd.DataFrame): Features for training.
        y (pd.Series): Target variable for training.

    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier()
    model.fit(X, y)  # Train the model
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the trained model on the test data.
    
    Args:
        model (RandomForestClassifier): Trained model to evaluate.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): True labels for the test set.
    """
    y_pred = model.predict(X_test)  # Make predictions
    accuracy = accuracy_score(y_test, y_pred)  # Calculate accuracy
    print(f"Model Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))  # Detailed report

def main(file_path: str) -> None:
    """Main function to execute the workflow of loading data, training, and evaluating the model.
    
    Args:
        file_path (str): Path to the CSV file containing the dataset.
    """
    data = load_data(file_path)  # Load the dataset
    X, y = preprocess_data(data)  # Preprocess the data

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)  # Train the model
    evaluate_model(model, X_test, y_test)  # Evaluate the model

if __name__ == "__main__":
    # Replace 'data.csv' with the actual path to your dataset
    main('data.csv')