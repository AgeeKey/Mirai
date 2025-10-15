"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-15T04:11:21.994876

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
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                        columns=iris['feature_names'] + ['target'])

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data and split into features and target.

    Args:
        df (pd.DataFrame): The input DataFrame containing the dataset.

    Returns:
        tuple: A tuple containing training and testing data.
    """
    X = df.iloc[:, :-1].values  # Features
    y = df.iloc[:, -1].values   # Target
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)  # Fit the model to the training data
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model's performance on the test set.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing target.
    """
    try:
        y_pred = model.predict(X_test)  # Make predictions
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except NotFittedError:
        print("Model is not fitted yet. Please train the model first.")

def main() -> None:
    """Main function to execute the workflow."""
    try:
        df = load_data()  # Load the dataset
        X_train, X_test, y_train, y_test = preprocess_data(df)  # Preprocess data
        model = train_model(X_train, y_train)  # Train the model
        evaluate_model(model, X_test, y_test)  # Evaluate the model
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()  # Execute the main function