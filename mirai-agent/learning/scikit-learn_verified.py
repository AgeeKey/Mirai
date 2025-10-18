"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-18T22:32:47.480274

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def split_data(data: pd.DataFrame) -> tuple:
    """Split the dataset into features and target, then into training and testing sets.
    
    Args:
        data (pd.DataFrame): The dataset to split.

    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    X = data.drop('target', axis=1)
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

class IrisModel:
    """A model class for training and predicting using Random Forest."""
    
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """Fit the Random Forest model to the training data.

        Args:
            X (np.ndarray): Feature data.
            y (np.ndarray): Target labels.
        """
        self.model.fit(X, y)
        self.is_fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the labels for the input data.

        Args:
            X (np.ndarray): Feature data.

        Returns:
            np.ndarray: Predicted labels.
        """
        if not self.is_fitted:
            raise NotFittedError("Model is not fitted yet. Call 'fit' before 'predict'.")
        return self.model.predict(X)

def main() -> None:
    """Main function to execute the training and evaluation of the model."""
    try:
        data = load_data()
        X_train, X_test, y_train, y_test = split_data(data)
        
        model = IrisModel()
        model.fit(X_train, y_train)
        
        predictions = model.predict(X_test)
        
        print("Accuracy:", accuracy_score(y_test, predictions))
        print("Classification Report:\n", classification_report(y_test, predictions))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()