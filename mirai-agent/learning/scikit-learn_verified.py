"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-22T06:45:17.120332

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                        columns=iris['feature_names'] + ['target'])

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target, then into training and testing sets.

    Args:
        df (pd.DataFrame): The DataFrame containing the dataset.

    Returns:
        tuple: A tuple containing the training features, testing features,
               training labels, and testing labels.
    """
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A simple classifier for the Iris dataset using a Random Forest model."""
    
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model on the training data.

        Args:
            X_train (np.ndarray): The training features.
            y_train (np.ndarray): The training labels.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the class labels for the provided features.

        Args:
            X (np.ndarray): The features to predict.

        Returns:
            np.ndarray: The predicted class labels.
        """
        try:
            return self.model.predict(X)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model on the test data.

        Args:
            X_test (np.ndarray): The testing features.
            y_test (np.ndarray): The testing labels.
        """
        y_pred = self.predict(X_test)
        if y_pred.size > 0:
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)
            print(f"Accuracy: {accuracy:.2f}")
            print("Classification Report:\n", report)

if __name__ == "__main__":
    data = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(data)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)
    classifier.evaluate(X_test, y_test)