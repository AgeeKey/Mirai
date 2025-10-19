"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.79
Tests Passed: 0/1
Learned: 2025-10-19T09:19:27.858959

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a pandas DataFrame."""
    try:
        iris = load_iris()
        data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        data['target'] = iris.target
        return data
    except Exception as e:
        logging.error("Error loading data: %s", e)
        raise

def split_data(data: pd.DataFrame) -> tuple:
    """Split the data into training and testing sets."""
    try:
        X = data.drop('target', axis=1)
        y = data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.error("Error splitting data: %s", e)
        raise

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest classifier on the training data."""
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        logging.error("Error training model: %s", e)
        raise

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the model and print the classification report and confusion matrix."""
    try:
        y_pred = model.predict(X_test)
        logging.info("Classification Report:\n%s", classification_report(y_test, y_pred))
        logging.info("Confusion Matrix:\n%s", confusion_matrix(y_test, y_pred))
    except Exception as e:
        logging.error("Error evaluating model: %s", e)
        raise

def main() -> None:
    """Main function to load data, train, and evaluate the model."""
    try:
        data = load_data()
        X_train, X_test, y_train, y_test = split_data(data)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        logging.critical("An error occurred in the main function: %s", e)

if __name__ == "__main__":
    main()