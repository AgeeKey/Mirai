"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 1/1
Learned: 2025-10-22T19:19:00.708199

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
    """
    Load the Iris dataset and return it as a pandas DataFrame.
    
    Returns:
        pd.DataFrame: The Iris dataset.
    """
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def split_data(data: pd.DataFrame) -> tuple:
    """
    Split the data into training and testing sets.
    
    Args:
        data (pd.DataFrame): The dataset to split.
    
    Returns:
        tuple: Training features, testing features, training labels, testing labels.
    """
    X = data.iloc[:, :-1]  # Features
    y = data.iloc[:, -1]   # Target
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisModel:
    def __init__(self):
        """
        Initialize the IrisModel with a RandomForestClassifier.
        """
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the model using the training data.
        
        Args:
            X_train (np.ndarray): The training features.
            y_train (np.ndarray): The training labels.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the labels for the test data.
        
        Args:
            X_test (np.ndarray): The testing features.
        
        Returns:
            np.ndarray: The predicted labels.
        """
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])

def main() -> None:
    """
    Main function to execute the model training and evaluation.
    """
    data = load_data()
    X_train, X_test, y_train, y_test = split_data(data)

    model = IrisModel()
    model.train(X_train, y_train)

    predictions = model.predict(X_test)

    if predictions.size > 0:
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print(classification_report(y_test, predictions))

if __name__ == "__main__":
    main()