"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-16T03:08:31.295791

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.

    :param file_path: Path to the CSV file
    :return: DataFrame containing the loaded data
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """
    Preprocess the data by splitting into features and target, and scaling the features.

    :param data: DataFrame containing the features and target
    :param target_column: Name of the target column
    :return: Tuple of (X, y) where X is the features and y is the target
    """
    try:
        X = data.drop(columns=[target_column])
        y = data[target_column]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        return X_scaled, y
    except KeyError as e:
        raise ValueError(f"Target column '{target_column}' not found: {e}")

def train_model(X: np.ndarray, y: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest classifier on the provided data.

    :param X: Feature matrix
    :param y: Target vector
    :return: Trained Random Forest classifier
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: pd.Series) -> None:
    """
    Evaluate the trained model and print the accuracy and classification report.

    :param model: Trained model
    :param X_test: Test feature matrix
    :param y_test: Test target vector
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print(classification_report(y_test, y_pred))

def main(file_path: str, target_column: str) -> None:
    """
    Main function to load data, preprocess it, train the model, and evaluate it.

    :param file_path: Path to the CSV file
    :param target_column: Name of the target column
    """
    data = load_data(file_path)
    X, y = preprocess_data(data, target_column)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Example usage
    main("data.csv", "target_column")