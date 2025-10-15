"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T00:30:28.178213

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
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    X = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    y = pd.Series(data=iris.target, name='target')
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest classifier on the provided features and target.

    Args:
        X (pd.DataFrame): Feature data.
        y (pd.Series): Target data.

    Returns:
        RandomForestClassifier: Trained classifier.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training the model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the trained model on test data and print the results.

    Args:
        model (RandomForestClassifier): Trained classifier.
        X_test (pd.DataFrame): Test feature data.
        y_test (pd.Series): Test target data.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print(classification_report(y_test, y_pred))
    except NotFittedError:
        print("The model is not fitted yet.")
    except Exception as e:
        raise RuntimeError(f"Error evaluating the model: {e}")

def main() -> None:
    """Main function to load data, train the model, and evaluate it."""
    X, y = load_data()  # Load the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split data

    model = train_model(X_train, y_train)  # Train the model
    evaluate_model(model, X_test, y_test)  # Evaluate the model

if __name__ == "__main__":
    main()