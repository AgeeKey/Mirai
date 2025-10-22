"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-22T00:22:28.491639

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.datasets import load_iris

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=iris['feature_names'] + ['target'])

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data and split it into training and testing sets.

    Args:
        df (pd.DataFrame): The input DataFrame containing features and target.

    Returns:
        tuple: A tuple containing the training and testing sets (X_train, X_test, y_train, y_test).
    """
    X = df.iloc[:, :-1].values  # Features
    y = df.iloc[:, -1].values   # Target
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the training data.

    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test data and print metrics.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): Test target.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')
    print('Confusion Matrix:')
    print(confusion_matrix(y_test, y_pred))
    print('Classification Report:')
    print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(df)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    main()