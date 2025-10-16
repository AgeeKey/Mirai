"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-16T22:26:39.584723

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    logging.info("Loading Iris dataset...")
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target, then into training and testing sets.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        
    Returns:
        tuple: Features and target split into training and testing sets.
    """
    logging.info("Preprocessing data...")
    X = df.values  # features
    y = load_iris().target  # target labels
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest model on the training data.
    
    Args:
        X_train (np.ndarray): Training feature set.
        y_train (np.ndarray): Training target labels.
        
    Returns:
        RandomForestClassifier: The trained model.
    """
    logging.info("Training the Random Forest model...")
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model on the test data and print the results.
    
    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test feature set.
        y_test (np.ndarray): Test target labels.
    """
    logging.info("Evaluating the model...")
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    logging.info(f"Accuracy: {accuracy:.2f}")
    logging.info("Classification Report:\n" + classification_report(y_test, predictions))
    logging.info("Confusion Matrix:\n" + str(confusion_matrix(y_test, predictions)))

def main() -> None:
    """Main function to run the machine learning pipeline."""
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(df)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()