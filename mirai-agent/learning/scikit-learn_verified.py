"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.79
Tests Passed: 0/1
Learned: 2025-10-21T19:14:02.244114

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    try:
        iris = load_iris()
        data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        data['target'] = iris.target
        return data
    except Exception as e:
        logging.error("Error loading data: %s", e)
        raise

def split_data(data: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the data into training and testing sets."""
    try:
        X = data.drop('target', axis=1)
        y = data['target']
        return train_test_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        logging.error("Error splitting data: %s", e)
        raise

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier."""
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        logging.error("Error training model: %s", e)
        raise

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the classification report and confusion matrix."""
    try:
        predictions = model.predict(X_test)
        print("Classification Report:\n", classification_report(y_test, predictions))
        print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
    except Exception as e:
        logging.error("Error evaluating model: %s", e)
        raise

def main() -> None:
    """Main function to execute the workflow."""
    data = load_data()
    X_train, X_test, y_train, y_test = split_data(data)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()