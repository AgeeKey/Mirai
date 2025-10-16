"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T12:40:46.378425

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a pandas DataFrame."""
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def preprocess_data(data: pd.DataFrame) -> tuple:
    """Split the data into features and target, then into training and testing sets.

    Args:
        data (pd.DataFrame): The input DataFrame containing features and target.

    Returns:
        tuple: The training features, testing features, training labels, testing labels.
    """
    X = data.iloc[:, :-1].values  # Features
    y = data.iloc[:, -1].values     # Target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the training data.

    Args:
        X_train (np.ndarray): The training features.
        y_train (np.ndarray): The training labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> float:
    """Evaluate the trained model on the testing data.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): The testing features.
        y_test (np.ndarray): The testing labels.

    Returns:
        float: The accuracy of the model on the test set.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy
    except NotFittedError as e:
        print("Model not fitted. Please train the model before evaluation.")
        raise e

def main() -> None:
    """Main function to load data, preprocess, train, and evaluate the model."""
    try:
        data = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(data)
        model = train_model(X_train, y_train)
        accuracy = evaluate_model(model, X_test, y_test)
        print(f'Model Accuracy: {accuracy:.2f}')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()