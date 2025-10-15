"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-15T13:37:48.632455

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
        pd.DataFrame: DataFrame containing the dataset.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except Exception as e:
        raise Exception(f"An error occurred while loading data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """Preprocess the dataset and split into features and target.

    Args:
        data (pd.DataFrame): The input data.
        target_column (str): The name of the target column.

    Returns:
        tuple: Features (X) and target (y) as numpy arrays.
    """
    if target_column not in data.columns:
        raise ValueError(f"The target column '{target_column}' is not in the DataFrame.")
    
    X = data.drop(columns=[target_column]).values
    y = data[target_column].values
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model.

    Args:
        X (np.ndarray): Features for training.
        y (np.ndarray): Target variable for training.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model and print accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): True labels for the test set.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main(file_path: str, target_column: str) -> None:
    """Main function to execute the ML pipeline.

    Args:
        file_path (str): Path to the dataset CSV.
        target_column (str): Name of the target column.
    """
    data = load_data(file_path)
    X, y = preprocess_data(data, target_column)
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Replace 'your_dataset.csv' and 'target' with your actual dataset file and target column
    main('your_dataset.csv', 'target')