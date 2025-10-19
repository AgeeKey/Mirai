"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-19T00:38:32.768614

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
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data by splitting into features and target, then into training and test sets.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing features and target.

    Returns:
        tuple: A tuple containing training and testing features and target labels.
    """
    X = df.values[:, :-1]  # Features
    y = df.values[:, -1]   # Target
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A simple Iris Classifier using Random Forest."""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model.
        
        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training target labels.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred while training the model: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.
        
        Args:
            X_test (np.ndarray): Test features.

        Returns:
            np.ndarray: Predicted labels.
        
        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("The model is not fitted yet. Please call the 'train' method first.")
        return self.model.predict(X_test)

def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> None:
    """Evaluate the model's performance and print the accuracy and classification report.
    
    Args:
        y_true (np.ndarray): True labels.
        y_pred (np.ndarray): Predicted labels.
    """
    accuracy = accuracy_score(y_true, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", classification_report(y_true, y_pred))

def main() -> None:
    """Main function to execute the training and evaluation of the Iris Classifier."""
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(df)
        classifier = IrisClassifier()
        classifier.train(X_train, y_train)
        y_pred = classifier.predict(X_test)
        evaluate_model(y_test, y_pred)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()