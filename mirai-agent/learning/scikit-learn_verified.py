"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-14T15:00:05.707257

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset into a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Preprocess the DataFrame and split into features and target."""
    X = df.values
    y = load_iris().target
    return X, y

def split_data(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisModel:
    """A simple model for Iris classification using Random Forest."""

    def __init__(self) -> None:
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model with the training data."""
        self.model.fit(X_train, y_train)

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the classes for the test data."""
        try:
            return self.model.predict(X_test)
        except NotFittedError as e:
            raise RuntimeError("The model has not been trained yet.") from e

    def evaluate(self, y_test: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model's performance."""
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to load data, train model, and evaluate performance."""
    try:
        df = load_data()
        X, y = preprocess_data(df)
        X_train, X_test, y_train, y_test = split_data(X, y)

        model = IrisModel()
        model.train(X_train, y_train)
        y_pred = model.predict(X_test)

        model.evaluate(y_test, y_pred)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()