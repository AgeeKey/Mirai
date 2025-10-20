"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T02:55:18.398775

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[pd.DataFrame, pd.Series]:
    """
    Load the Iris dataset and return features and target.

    Returns:
        Tuple[pd.DataFrame, pd.Series]: Features and target variable.
    """
    iris = load_iris()
    X = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    y = pd.Series(data=iris.target, name='species')
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest model on the provided features and target.

    Args:
        X (pd.DataFrame): Features for training.
        y (pd.Series): Target variable for training.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        print(f"Error during model training: {e}")
        raise

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate the trained model on the test set.

    Args:
        model (RandomForestClassifier): Trained model to evaluate.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): True labels for the test set.
    """
    try:
        y_pred = model.predict(X_test)
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
    except Exception as e:
        print(f"Error during model evaluation: {e}")
        raise

def main() -> None:
    """
    Main function to execute the training and evaluation of the model.
    """
    X, y = load_data()  # Load the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split the data
    
    model = train_model(X_train, y_train)  # Train the model
    evaluate_model(model, X_test, y_test)  # Evaluate the model

if __name__ == "__main__":
    main()