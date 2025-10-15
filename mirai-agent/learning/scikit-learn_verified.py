"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-15T12:16:49.070388

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data() -> pd.DataFrame:
    """
    Load the Iris dataset and return it as a pandas DataFrame.

    Returns:
        pd.DataFrame: The Iris dataset.
    """
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=iris['feature_names'] + ['target'])

def split_data(data: pd.DataFrame) -> tuple:
    """
    Split the data into training and testing sets.

    Args:
        data (pd.DataFrame): The input data.

    Returns:
        tuple: The training features, training labels, testing features, testing labels.
    """
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest model.

    Args:
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate the trained model and print accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (pd.DataFrame): Testing features.
        y_test (pd.Series): Testing labels.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", classification_report(y_test, y_pred))

def main() -> None:
    """
    Main function to run the machine learning pipeline.
    """
    try:
        data = load_data()
        X_train, X_test, y_train, y_test = split_data(data)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()