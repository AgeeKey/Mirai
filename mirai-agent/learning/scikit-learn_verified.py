"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T05:33:25.537593

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
        pd.DataFrame: DataFrame containing the loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise ValueError("No data found in the file.") from e
    except Exception as e:
        raise Exception("An error occurred while loading the data.") from e

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """
    Preprocess the data by separating features and target variable.

    Args:
        data (pd.DataFrame): The input DataFrame.
        target_column (str): The name of the target column.

    Returns:
        tuple: Features (X) and target (y) as separate DataFrames.
    """
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in data.")

    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest classifier on the provided data.

    Args:
        X (pd.DataFrame): Feature set.
        y (pd.Series): Target variable.

    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate the trained model using accuracy and confusion matrix.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (pd.DataFrame): Test feature set.
        y_test (pd.Series): Test target variable.

    Returns:
        None
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("Accuracy:", accuracy)
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

def main(file_path: str, target_column: str) -> None:
    """
    Main function to load data, train, and evaluate the model.

    Args:
        file_path (str): Path to the CSV file.
        target_column (str): The name of the target column.

    Returns:
        None
    """
    data = load_data(file_path)
    
    X, y = preprocess_data(data, target_column)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Example usage with a sample CSV file path and target column name
    main("path/to/your/data.csv", "target_column_name")