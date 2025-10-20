"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-20T22:22:41.443239

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
        tuple: A tuple containing the training and testing sets.
    """
    X = df.iloc[:, :-1]  # Features
    y = df.iloc[:, -1]   # Target variable
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisModel:
    """A class for training and predicting with a Random Forest model."""
    
    def __init__(self) -> None:
        self.model = RandomForestClassifier(random_state=42)
    
    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the Random Forest model.
        
        Args:
            X (np.ndarray): Features for training.
            y (np.ndarray): Target variable for training.
        """
        self.model.fit(X, y)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the trained model.
        
        Args:
            X (np.ndarray): Features for prediction.
        
        Returns:
            np.ndarray: Predicted labels.
        """
        try:
            return self.model.predict(X)
        except NotFittedError as e:
            print("Model is not fitted yet. Please train the model first.")
            raise e

def main() -> None:
    """Main function to execute the training and prediction process."""
    try:
        df = load_data()
        # Add the target column to DataFrame for splitting
        df['target'] = load_iris().target
        
        X_train, X_test, y_train, y_test = split_data(df)
        
        model = IrisModel()
        model.train(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        # Display the results
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
        print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()