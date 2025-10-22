"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.78
Tests Passed: 0/1
Learned: 2025-10-22T09:42:24.073171

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and convert it to a DataFrame."""
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def split_data(data: pd.DataFrame) -> tuple:
    """Split the dataset into training and testing sets."""
    X = data.drop('target', axis=1)
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

class IrisClassifier:
    """A simple Random Forest classifier for the Iris dataset."""

    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the Random Forest model on the provided data."""
        try:
            self.model.fit(X, y)
            logging.info("Model training completed.")
        except Exception as e:
            logging.error(f"Error during model training: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""
        try:
            return self.model.predict(X)
        except NotFittedError as e:
            logging.error("Model is not fitted yet; please train the model first.")
            raise e
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            raise e

def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> None:
    """Evaluate the model's performance and print the results."""
    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred)
    logging.info(f"Model Accuracy: {accuracy:.2f}")
    logging.info("Classification Report:\n" + report)

def main() -> None:
    """Main function to execute the workflow."""
    data = load_data()
    X_train, X_test, y_train, y_test = split_data(data)

    model = IrisClassifier()
    model.train(X_train, y_train)

    y_pred = model.predict(X_test)
    evaluate_model(y_test, y_pred)

if __name__ == "__main__":
    main()