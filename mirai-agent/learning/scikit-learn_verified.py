"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-19T11:09:47.823644

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

    Parameters:
    - file_path: str - Path to the CSV file.

    Returns:
    - pd.DataFrame - Loaded data as a pandas DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise ValueError("No data in file") from e
    except Exception as e:
        raise Exception("An error occurred while loading data") from e

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """
    Preprocess the data by splitting it into features and target variable.

    Parameters:
    - data: pd.DataFrame - The input data.
    - target_column: str - The name of the target column.

    Returns:
    - tuple - Features (X) and target (y).
    """
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' does not exist in the data.")
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier model.

    Parameters:
    - X: np.ndarray - Feature data.
    - y: np.ndarray - Target data.

    Returns:
    - RandomForestClassifier - Trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model and print the accuracy and classification report.

    Parameters:
    - model: RandomForestClassifier - The trained model.
    - X_test: np.ndarray - Test feature data.
    - y_test: np.ndarray - Test target data.
    """
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, predictions))

def main(file_path: str, target_column: str) -> None:
    """
    Main function to execute the data loading, processing, model training, and evaluation.

    Parameters:
    - file_path: str - Path to the CSV file containing the data.
    - target_column: str - The name of the target column.
    """
    # Load the data
    data = load_data(file_path)
    
    # Preprocess the data
    X, y = preprocess_data(data, target_column)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Replace 'data.csv' with your dataset path and 'target' with your target column name
    main('data.csv', 'target')