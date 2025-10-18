"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-18T20:58:36.850388

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
from sklearn.datasets import load_iris

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def preprocess_data(data: pd.DataFrame) -> tuple:
    """Preprocess the data for training and testing.
    
    Args:
        data (pd.DataFrame): The input data with features and target.
    
    Returns:
        tuple: A tuple containing training and testing data.
    """
    X = data.drop(columns='target')
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

class IrisModel:
    """A simple classifier for the Iris dataset using Random Forest."""

    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Train the Random Forest model on the training data.
        
        Args:
            X_train (pd.DataFrame): Features for training.
            y_train (pd.Series): Target for training.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions using the trained model.
        
        Args:
            X (pd.DataFrame): Features for prediction.
        
        Returns:
            np.ndarray: Predicted labels.
        
        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, 'estimators_'):
            raise NotFittedError("This IrisModel instance is not fitted yet.")
        return self.model.predict(X)

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> None:
        """Evaluate the model's performance on the test data.
        
        Args:
            X_test (pd.DataFrame): Features for testing.
            y_test (pd.Series): True labels for testing.
        """
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)

def main() -> None:
    """Main function to execute the model training and evaluation."""
    try:
        data = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(data)
        
        model = IrisModel()
        model.train(X_train, y_train)
        model.evaluate(X_test, y_test)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()