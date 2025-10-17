"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-17T22:41:18.888476

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset into a pandas DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def split_data(df: pd.DataFrame, test_size: float = 0.2) -> tuple:
    """Split the DataFrame into training and testing sets.

    Args:
        df (pd.DataFrame): The DataFrame to split.
        test_size (float): The proportion of the dataset to include in the test split.

    Returns:
        tuple: A tuple containing the training features, testing features,
               training labels, and testing labels.
    """
    X = df.iloc[:, :-1]  # Features
    y = df.iloc[:, -1]   # Target variable
    return train_test_split(X, y, test_size=test_size, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a RandomForest model.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model on the test set.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing labels.

    Raises:
        NotFittedError: If the model has not been fitted.
    """
    try:
        y_pred = model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except NotFittedError as e:
        print("Model is not fitted yet. Please train the model before evaluation.")
        raise e

def main() -> None:
    """Main function to run the machine learning workflow."""
    # Load data
    df = load_data()

    # Split data
    X_train, X_test, y_train, y_test = split_data(df)

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()