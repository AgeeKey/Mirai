"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T10:24:47.024070

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(filepath: str) -> pd.DataFrame:
    """Load dataset from a CSV file."""
    try:
        data = pd.read_csv(filepath)
        return data
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """Preprocess the data by separating features and target."""
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in data.")
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest model."""
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the model and print accuracy and classification report."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main(filepath: str, target_column: str) -> None:
    """Main function to load data, train, and evaluate the model."""
    data = load_data(filepath)
    X, y = preprocess_data(data, target_column)

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Example usage: adjust the filepath and target_column as needed
    filepath = 'path/to/your/data.csv'
    target_column = 'target'
    main(filepath, target_column)