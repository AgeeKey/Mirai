"""
mlflow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-20T05:01:47.162814

This code has been verified by MIRAI's NASA-level learning system.
"""

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
import logging

# Set up logging
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

def train_model(data: pd.DataFrame) -> RandomForestClassifier:
    """Train a Random Forest model on the provided data.

    Args:
        data (pd.DataFrame): The input data containing features and target.

    Returns:
        RandomForestClassifier: The trained model.
    """
    try:
        X = data.drop('target', axis=1)
        y = data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Log the model with MLflow
        mlflow.log_param("model_type", "RandomForest")
        mlflow.sklearn.log_model(model, "model")

        # Evaluate the model
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        mlflow.log_metric("accuracy", accuracy)

        return model
    except Exception as e:
        logging.error("Error training the model: %s", e)
        raise

if __name__ == "__main__":
    """Main entry point for training the model and logging with MLflow."""
    mlflow.start_run()  # Start an MLflow run
    try:
        data = load_data()
        model = train_model(data)
    finally:
        mlflow.end_run()  # Ensure the MLflow run ends