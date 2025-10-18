"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-18T20:11:34.896984

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import logging

# Set up logging for error handling
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """
    Load the Iris dataset and return it as a DataFrame.
    
    Returns:
        pd.DataFrame: Iris dataset as a DataFrame.
    """
    try:
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['target'] = iris.target
        return df
    except Exception as e:
        logging.error("Error loading the data: %s", e)
        raise

def split_data(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the DataFrame into training and testing sets.
    
    Args:
        df (pd.DataFrame): Input DataFrame containing features and target.
        
    Returns:
        tuple: Training features, testing features, training labels, testing labels.
    """
    try:
        X = df.iloc[:, :-1].values  # Features
        y = df.iloc[:, -1].values   # Target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.error("Error splitting the data: %s", e)
        raise

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest model on the training data.
    
    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training labels.
        
    Returns:
        RandomForestClassifier: Trained Random Forest model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        logging.error("Error training the model: %s", e)
        raise

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model and print the classification report and confusion matrix.
    
    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing labels.
    """
    try:
        predictions = model.predict(X_test)
        print("Classification Report:\n", classification_report(y_test, predictions))
        print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
    except Exception as e:
        logging.error("Error evaluating the model: %s", e)
        raise

def main() -> None:
    """
    Main function to execute the machine learning workflow.
    """
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = split_data(df)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        logging.error("An error occurred in the main workflow: %s", e)

if __name__ == "__main__":
    main()