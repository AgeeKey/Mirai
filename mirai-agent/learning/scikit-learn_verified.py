"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T03:58:23.063201

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
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """
    Preprocess the data by splitting it into features and labels, and then into training and testing sets.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing the dataset.
        
    Returns:
        tuple: A tuple containing the training and testing data (X_train, X_test, y_train, y_test).
    """
    X = df.values
    y = load_iris().target
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisModel:
    def __init__(self) -> None:
        """Initialize the IrisModel with a RandomForestClassifier."""
        self.model = RandomForestClassifier()
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the Random Forest model on the training data.
        
        Args:
            X_train (np.ndarray): The training features.
            y_train (np.ndarray): The training labels.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"Error during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the labels for the test data.
        
        Args:
            X_test (np.ndarray): The test features.
            
        Returns:
            np.ndarray: The predicted labels.
        """
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])

def evaluate_model(y_test: np.ndarray, y_pred: np.ndarray) -> None:
    """
    Evaluate the model's performance using accuracy score and classification report.
    
    Args:
        y_test (np.ndarray): The true labels for the test set.
        y_pred (np.ndarray): The predicted labels.
    """
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to run the Iris classification model."""
    df = load_data()  # Load the dataset
    X_train, X_test, y_train, y_test = preprocess_data(df)  # Preprocess data
    
    model = IrisModel()  # Initialize model
    model.train(X_train, y_train)  # Train the model
    
    y_pred = model.predict(X_test)  # Make predictions
    evaluate_model(y_test, y_pred)  # Evaluate the model

if __name__ == "__main__":
    main()  # Execute the main function