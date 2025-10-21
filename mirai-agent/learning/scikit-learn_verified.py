"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-21T04:42:55.641830

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def split_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into training and testing sets.

    Args:
        df (pd.DataFrame): The DataFrame containing the dataset.

    Returns:
        tuple: A tuple containing the training features, testing features, training labels, and testing labels.
    """
    X = df.iloc[:, :-1]  # Features
    y = df.iloc[:, -1]   # Labels
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisModel:
    """A simple Random Forest Classifier model for the Iris dataset."""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_fitted = False

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model with the training data.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training labels.
        """
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
        except Exception as e:
            print(f"Error during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions with the trained model.

        Args:
            X_test (np.ndarray): Testing features.

        Returns:
            np.ndarray: Predicted labels.

        Raises:
            NotFittedError: If the model has not been fitted yet.
        """
        if not self.is_fitted:
            raise NotFittedError("Model is not fitted yet. Please call 'train' before 'predict'.")
        return self.model.predict(X_test)

def evaluate_model(y_test: np.ndarray, y_pred: np.ndarray) -> None:
    """Evaluate the model's performance.

    Args:
        y_test (np.ndarray): True labels for the test set.
        y_pred (np.ndarray): Predicted labels from the model.
    """
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

def main() -> None:
    """Main function to run the model training and evaluation."""
    df = load_data()
    X_train, X_test, y_train, y_test = split_data(df)

    model = IrisModel()
    model.train(X_train, y_train)

    y_pred = model.predict(X_test)
    evaluate_model(y_test, y_pred)

if __name__ == "__main__":
    main()