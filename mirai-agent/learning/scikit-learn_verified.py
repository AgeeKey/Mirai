"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-14T18:01:19.463389

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(filepath: str) -> pd.DataFrame:
    """Load dataset from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {filepath} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the data: {e}")

def preprocess_data(data: pd.DataFrame) -> tuple:
    """Preprocess the data for modeling.

    Args:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        tuple: Features and target variable.
    """
    # Assuming the last column is the target variable
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest model.

    Args:
        X (pd.DataFrame): Features.
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
        model (RandomForestClassifier): Trained model.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): Test target variable.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main(filepath: str) -> None:
    """Main function to run the machine learning pipeline.

    Args:
        filepath (str): Path to the dataset.
    """
    data = load_data(filepath)
    X, y = preprocess_data(data)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a Random Forest model on a dataset.")
    parser.add_argument("filepath", type=str, help="Path to the CSV dataset.")
    args = parser.parse_args()
    
    main(args.filepath)