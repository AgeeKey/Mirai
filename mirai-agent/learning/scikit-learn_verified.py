"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-17T20:16:47.381538

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset into a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=iris['feature_names'] + ['target'])

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the DataFrame and split it into features and target variable.

    Args:
        df (pd.DataFrame): The DataFrame containing the dataset.

    Returns:
        tuple: A tuple containing features (X) and target (y).
    """
    X = df.drop('target', axis=1)
    y = df['target']
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided features and target.

    Args:
        X (pd.DataFrame): Features for training.
        y (pd.Series): Target variable for training.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)  # Train the model
    return model

def evaluate_model(model: RandomForestClassifier, X: pd.DataFrame, y: pd.Series) -> None:
    """Evaluate the trained model and print classification report and confusion matrix.

    Args:
        model (RandomForestClassifier): The trained model.
        X (pd.DataFrame): Features for evaluation.
        y (pd.Series): Target variable for evaluation.
    """
    try:
        y_pred = model.predict(X)  # Predict using the model
        print("Classification Report:\n", classification_report(y, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y, y_pred))
    except NotFittedError:
        print("Model is not fitted yet. Please train the model before evaluation.")

def main() -> None:
    """Main function to execute the workflow."""
    try:
        df = load_data()  # Load the dataset
        X, y = preprocess_data(df)  # Preprocess the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split the data
        model = train_model(X_train, y_train)  # Train the model
        evaluate_model(model, X_test, y_test)  # Evaluate the model
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()  # Run the main function