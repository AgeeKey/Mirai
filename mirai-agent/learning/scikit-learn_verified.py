"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T01:09:52.087638

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """Preprocess the data for training.

    Args:
        data (pd.DataFrame): The input dataset.
        target_column (str): The name of the target column.

    Returns:
        tuple: Features (X) and target (y).
    """
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in the dataset.")
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest Classifier.

    Args:
        X (pd.DataFrame): Features for training.
        y (pd.Series): Target variable.

    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the trained model.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (pd.DataFrame): Features for testing.
        y_test (pd.Series): True labels for testing.
    """
    predictions = model.predict(X_test)
    print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
    print("\nClassification Report:\n", classification_report(y_test, predictions))

def main(file_path: str, target_column: str) -> None:
    """Main function to execute the workflow.

    Args:
        file_path (str): Path to the CSV file.
        target_column (str): Name of the target column.
    """
    data = load_data(file_path)
    X, y = preprocess_data(data, target_column)
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Example usage
    main("path/to/your/data.csv", "target_column_name")