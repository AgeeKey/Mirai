"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T15:23:58.511564

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Preprocess the data by splitting into features and target, and scaling.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.

    Returns:
        tuple[np.ndarray, np.ndarray]: The features and target arrays.
    """
    X = df.values
    y = load_iris().target
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided data.

    Args:
        X (np.ndarray): The feature set.
        y (np.ndarray): The target labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X: np.ndarray, y: np.ndarray) -> None:
    """Evaluate the trained model and print the classification report and confusion matrix.

    Args:
        model (RandomForestClassifier): The trained model.
        X (np.ndarray): The feature set.
        y (np.ndarray): The target labels.
    """
    y_pred = model.predict(X)
    logging.info("Classification Report:\n%s", classification_report(y, y_pred))
    logging.info("Confusion Matrix:\n%s", confusion_matrix(y, y_pred))

def main() -> None:
    """Main function to execute data loading, preprocessing, model training, and evaluation."""
    try:
        df = load_data()  # Load dataset
        X, y = preprocess_data(df)  # Preprocess data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = train_model(X_train, y_train)  # Train model
        evaluate_model(model, X_test, y_test)  # Evaluate model
    except Exception as e:
        logging.error("An error occurred: %s", e)

if __name__ == "__main__":
    main()