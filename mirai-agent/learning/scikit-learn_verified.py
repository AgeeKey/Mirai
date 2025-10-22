"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T06:29:14.520493

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """
    Load the Iris dataset and return it as a DataFrame.

    Returns:
        pd.DataFrame: The Iris dataset.
    """
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """
    Preprocess the data by splitting it into training and testing sets.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        tuple: Features and target variables for training and testing.
    """
    X = df.values
    y = load_iris().target
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest classifier on the training data.

    Args:
        X_train (np.ndarray): The training features.
        y_train (np.ndarray): The training labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model on the test data and print the results.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): The test features.
        y_test (np.ndarray): The test labels.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except NotFittedError as e:
        print("Model not fitted yet. Error:", e)

def main() -> None:
    """
    Main function to run the entire machine learning pipeline.
    """
    try:
        df = load_data()  # Load the dataset
        X_train, X_test, y_train, y_test = preprocess_data(df)  # Preprocess the data
        model = train_model(X_train, y_train)  # Train the model
        evaluate_model(model, X_test, y_test)  # Evaluate the model
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()  # Execute the main function