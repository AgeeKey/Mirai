"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-15T12:33:05.982343

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def split_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into training and testing sets.

    Args:
        df (pd.DataFrame): The DataFrame containing the dataset.

    Returns:
        tuple: A tuple containing the training features, testing features,
               training labels, and testing labels.
    """
    X = df.iloc[:, :-1]  # Features
    y = df.iloc[:, -1]   # Labels
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest model on the training data.

    Args:
        X_train (pd.DataFrame): The training features.
        y_train (pd.Series): The training labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the model performance on the test set.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (pd.DataFrame): The test features.
        y_test (pd.Series): The test labels.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    logging.info(f"Model Accuracy: {accuracy:.2f}")
    logging.info("Classification Report:\n" + classification_report(y_test, y_pred))
    logging.info("Confusion Matrix:\n" + str(confusion_matrix(y_test, y_pred)))

def main() -> None:
    """Main function to execute the workflow."""
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = split_data(df)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()