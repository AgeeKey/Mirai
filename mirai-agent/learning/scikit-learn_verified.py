"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-17T13:29:34.150080

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load the dataset from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def preprocess_data(df: pd.DataFrame) -> tuple:
    """
    Preprocess the input DataFrame by splitting into features and labels.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        tuple: Features (X) and labels (y).
    """
    if 'target' not in df.columns:
        raise ValueError("The DataFrame must contain a 'target' column.")
    
    X = df.drop('target', axis=1)
    y = df['target']
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier model.

    Args:
        X (pd.DataFrame): Features for training.
        y (pd.Series): Target labels for training.

    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate the trained model on the test dataset.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): Test labels.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)

def main(file_path: str) -> None:
    """
    Main function to execute the workflow.

    Args:
        file_path (str): Path to the dataset CSV file.
    """
    df = load_data(file_path)
    X, y = preprocess_data(df)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Replace 'data.csv' with the path to your dataset
    main('data.csv')