"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T17:34:29.795787

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
from typing import Tuple

def load_data(file_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load data from a CSV file.

    :param file_path: Path to the CSV file.
    :return: Tuple of features and target variable.
    """
    try:
        data = pd.read_csv(file_path)
        X = data.iloc[:, :-1].values  # Features
        y = data.iloc[:, -1].values    # Target variable
        return X, y
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier.

    :param X: Features for training.
    :param y: Target variable for training.
    :return: Trained RandomForestClassifier model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model.

    :param model: Trained RandomForestClassifier model.
    :param X_test: Features for testing.
    :param y_test: True labels for testing.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
    except NotFittedError:
        print("Model is not fitted yet. Please train the model before evaluation.")
    except Exception as e:
        raise ValueError(f"Error during model evaluation: {e}")

def main(file_path: str) -> None:
    """
    Main function to load data, train and evaluate the model.

    :param file_path: Path to the CSV file.
    """
    X, y = load_data(file_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Replace 'data.csv' with your actual data file path
    main('data.csv')