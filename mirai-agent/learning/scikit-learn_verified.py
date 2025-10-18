"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-18T11:05:11.000781

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
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {filepath} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """Preprocess the data by separating features and target."""
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not in DataFrame.")
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier."""
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on test data."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main(filepath: str, target_column: str) -> None:
    """Main function to run the machine learning pipeline."""
    data = load_data(filepath)
    X, y = preprocess_data(data, target_column)
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Example usage with a sample CSV file and target column
    main("sample_data.csv", "target_column_name")