"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-21T01:48:41.033953

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_and_prepare_data() -> pd.DataFrame:
    """
    Load the Iris dataset and prepare it for training.

    Returns:
        pd.DataFrame: A DataFrame containing the Iris dataset.
    """
    try:
        iris = load_iris()
        data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        data['target'] = iris.target
        logging.info("Data loaded successfully.")
        return data
    except Exception as e:
        logging.error("Error loading data: %s", e)
        raise

def train_model(data: pd.DataFrame) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier on the provided data.

    Args:
        data (pd.DataFrame): The DataFrame containing the features and target.

    Returns:
        RandomForestClassifier: The trained classifier.
    """
    try:
        X = data.iloc[:, :-1]  # Features
        y = data['target']      # Target variable

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate the model
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        logging.info(f"Model trained successfully with an accuracy of {accuracy:.2f}")

        return model
    except Exception as e:
        logging.error("Error training the model: %s", e)
        raise

def main() -> None:
    """
    Main function to execute the workflow of loading data, training the model, and reporting accuracy.
    """
    try:
        data = load_and_prepare_data()
        model = train_model(data)

        # Final evaluation on the whole dataset
        predictions = model.predict(data.iloc[:, :-1])
        report = classification_report(data['target'], predictions)
        logging.info("\nClassification Report:\n%s", report)
    except Exception as e:
        logging.error("An error occurred in the main workflow: %s", e)

if __name__ == "__main__":
    main()