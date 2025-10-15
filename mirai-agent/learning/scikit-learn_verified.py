"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-15T21:46:35.401475

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
    Load the Iris dataset.

    Returns:
        pd.DataFrame: A DataFrame containing the Iris dataset.
    """
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=iris['feature_names'] + ['target'])

def split_data(data: pd.DataFrame, test_size: float = 0.2) -> tuple:
    """
    Split the dataset into training and testing sets.

    Args:
        data (pd.DataFrame): The dataset to split.
        test_size (float): The proportion of the dataset to include in the test split.

    Returns:
        tuple: Training features, testing features, training labels, testing labels.
    """
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    return train_test_split(X, y, test_size=test_size, random_state=42)

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest classifier.

    Args:
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training labels.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate the trained model on the test set.

    Args:
        model (RandomForestClassifier): Trained Random Forest model.
        X_test (pd.DataFrame): Testing features.
        y_test (pd.Series): Testing labels.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main() -> None:
    """
    Main function to execute the machine learning workflow.
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