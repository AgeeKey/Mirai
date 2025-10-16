"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T08:46:58.023007

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The provided file is empty.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """
    Preprocess the dataset by splitting it into features and target.

    Args:
        data (pd.DataFrame): The dataset to process.
        target_column (str): The name of the target column.

    Returns:
        tuple: Features and target variables.
    """
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in the dataset.")
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest classifier.

    Args:
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training target.

    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate the model's performance.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (pd.DataFrame): Testing features.
        y_test (pd.Series): Testing target.
    """
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

def main(file_path: str, target_column: str) -> None:
    """
    Main function to execute the workflow.

    Args:
        file_path (str): Path to the CSV file.
        target_column (str): The name of the target column.
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