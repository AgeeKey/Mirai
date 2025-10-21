"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-21T01:32:46.097124

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data by splitting it into features and target variable.

    Args:
        df (pd.DataFrame): The input DataFrame containing features.

    Returns:
        tuple: Features and target variable split.
    """
    X = df.values  # Features
    y = load_iris().target  # Target variable
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a RandomForestClassifier on the provided features and target.

    Args:
        X (np.ndarray): Features for training.
        y (np.ndarray): Target for training.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X: np.ndarray, y: np.ndarray) -> None:
    """Evaluate the trained model and print the accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model.
        X (np.ndarray): Features for evaluation.
        y (np.ndarray): True labels for evaluation.
    """
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    print(f'Accuracy: {accuracy:.2f}')
    print('Classification Report:\n', classification_report(y, y_pred))

def main() -> None:
    """Main function to load data, preprocess, train, and evaluate the model."""
    try:
        df = load_data()
        X, y = preprocess_data(df)
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    main()