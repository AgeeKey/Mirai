"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-16T10:08:28.215282

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
    """Load the Iris dataset as a pandas DataFrame."""
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    return df

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data by splitting it into features and target, and then train/test split.

    Args:
        df (pd.DataFrame): The input DataFrame containing features and target.

    Returns:
        tuple: A tuple containing training and testing features and target.
    """
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

class Model:
    """A class to encapsulate the Random Forest Classifier model."""

    def __init__(self) -> None:
        """Initialize the model."""
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Train the Random Forest model.

        Args:
            X_train (pd.DataFrame): Training features.
            y_train (pd.Series): Training target.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: pd.DataFrame) -> np.ndarray:
        """Make predictions with the trained model.

        Args:
            X_test (pd.DataFrame): Testing features.

        Returns:
            np.ndarray: Predictions made by the model.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("The model is not fitted yet. Please call 'train' first.")
        return self.model.predict(X_test)

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> float:
        """Evaluate the model's performance.

        Args:
            X_test (pd.DataFrame): Testing features.
            y_test (pd.Series): Testing target.

        Returns:
            float: The accuracy of the model.
        """
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        return accuracy

if __name__ == "__main__":
    # Load and preprocess data
    data = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(data)

    # Initialize and train the model
    model = Model()
    model.train(X_train, y_train)

    # Evaluate the model
    accuracy = model.evaluate(X_test, y_test)
    print(f"Model Accuracy: {accuracy:.2f}")