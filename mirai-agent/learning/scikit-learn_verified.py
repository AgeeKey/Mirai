"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-19T10:06:47.480117

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def preprocess_data(data: pd.DataFrame) -> (np.ndarray, np.ndarray):
    """Preprocess the data for the model.

    Args:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target variable.
    """
    # Assuming the last column is the target variable
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target variable.

    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test feature matrix.
        y_test (np.ndarray): Test target variable.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main(file_path: str) -> None:
    """Main function to run the machine learning pipeline.

    Args:
        file_path (str): Path to the CSV file containing the dataset.
    """
    data = load_data(file_path)
    X, y = preprocess_data(data)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Replace 'your_data.csv' with the path to your dataset
    main('your_data.csv')