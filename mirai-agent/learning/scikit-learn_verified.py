"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-22T14:00:54.352303

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    try:
        iris = load_iris()
        return pd.DataFrame(data=iris.data, columns=iris.feature_names)
    except Exception as e:
        raise RuntimeError("Failed to load data") from e

def prepare_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target variable, then into train and test sets."""
    try:
        X = df.values
        y = np.array(load_iris().target)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        raise ValueError("Failed to prepare data") from e

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the training data."""
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError("Failed to train model") from e

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model on the test data and print the accuracy and classification report."""
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, predictions))
    except Exception as e:
        raise RuntimeError("Failed to evaluate model") from e

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = prepare_data(df)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()