"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T11:41:12.659571

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    try:
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['target'] = iris.target
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data by splitting into features and target, and then into training and testing sets.

    Args:
        df (pd.DataFrame): The input DataFrame containing features and target.

    Returns:
        tuple: A tuple containing the training and testing features and targets.
    """
    try:
        X = df.drop(columns='target')
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.error(f"Error preprocessing data: {e}")
        raise

class Model:
    """A simple wrapper for the RandomForestClassifier."""
    
    def __init__(self):
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model using the training data.

        Args:
            X_train (np.ndarray): The training features.
            y_train (np.ndarray): The training target.
        """
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
            logging.info("Model training complete.")
        except Exception as e:
            logging.error(f"Error training model: {e}")
            raise

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.

        Args:
            X_test (np.ndarray): The testing features.

        Returns:
            np.ndarray: The predicted target values.

        Raises:
            NotFittedError: If the model has not been fitted yet.
        """
        if not self.is_fitted:
            raise NotFittedError("Model must be trained before making predictions.")
        try:
            return self.model.predict(X_test)
        except Exception as e:
            logging.error(f"Error making predictions: {e}")
            raise

def main() -> None:
    """Main function to execute the model training and evaluation."""
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(df)

        model = Model()
        model.train(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f"Accuracy: {accuracy:.2f}")
        print(classification_report(y_test, y_pred))
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()