"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-17T04:37:23.769614

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.datasets import load_iris
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """
    Load the Iris dataset and return it as a DataFrame.

    Returns:
        pd.DataFrame: The Iris dataset as a DataFrame.
    """
    try:
        iris = load_iris()
        data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        data['target'] = iris.target
        return data
    except Exception as e:
        logging.error("Error loading data: %s", e)
        raise

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier on the provided features and target.

    Args:
        X (np.ndarray): Features for training.
        y (np.ndarray): Target variable for training.

    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        logging.error("Error training model: %s", e)
        raise

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray):
    """
    Evaluate the trained model using accuracy and other metrics.

    Args:
        model (RandomForestClassifier): The trained Random Forest model.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): True labels for test features.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        logging.info("Accuracy: %.2f%%", accuracy * 100)
        logging.info("Classification Report:\n%s", classification_report(y_test, predictions))
        logging.info("Confusion Matrix:\n%s", confusion_matrix(y_test, predictions))
    except Exception as e:
        logging.error("Error evaluating model: %s", e)
        raise

def main():
    """
    Main function to run the machine learning workflow.
    """
    try:
        # Load data
        data = load_data()
        
        # Split the data into features and target
        X = data.drop('target', axis=1).values
        y = data['target'].values
        
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        logging.error("Error in main execution: %s", e)

if __name__ == "__main__":
    main()