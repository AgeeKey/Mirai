"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T11:05:18.552016

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def split_data(df: pd.DataFrame, test_size: float = 0.2) -> tuple:
    """Split the DataFrame into training and test sets.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing features.
        test_size (float): The proportion of the dataset to include in the test split.
    
    Returns:
        tuple: A tuple containing the training features, test features, training labels, and test labels.
    """
    X = df.values[:, :-1]  # Features
    y = df.values[:, -1]   # Labels
    return train_test_split(X, y, test_size=test_size, random_state=42)

class IrisClassifier:
    """A simple Iris classification model using Random Forest."""

    def __init__(self) -> None:
        self.model = RandomForestClassifier()

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the Random Forest model.
        
        Args:
            X (np.ndarray): Training features.
            y (np.ndarray): Training labels.
        """
        logging.info("Training the model...")
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.
        
        Args:
            X (np.ndarray): Input features for prediction.
        
        Returns:
            np.ndarray: Predicted labels.
        
        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not self.is_fitted():
            raise NotFittedError("The model is not fitted yet.")
        return self.model.predict(X)

    def is_fitted(self) -> bool:
        """Check if the model is fitted.
        
        Returns:
            bool: True if the model is fitted, False otherwise.
        """
        return hasattr(self.model, "estimators_")

def main() -> None:
    """Main function to execute the workflow."""
    try:
        # Load data
        df = load_data()
        
        # Split data
        X_train, X_test, y_train, y_test = split_data(df)
        
        # Initialize and train classifier
        classifier = IrisClassifier()
        classifier.train(X_train, y_train)
        
        # Make predictions
        predictions = classifier.predict(X_test)
        
        # Evaluate model
        print(confusion_matrix(y_test, predictions))
        print(classification_report(y_test, predictions))
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()