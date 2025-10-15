"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.79
Tests Passed: 0/1
Learned: 2025-10-15T02:01:49.916699

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

# Setup logging configuration
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    try:
        iris = load_iris()
        return pd.DataFrame(data=iris.data, columns=iris.feature_names).assign(target=iris.target)
    except Exception as e:
        logging.error("Error loading data: %s", e)
        raise

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data: split into features and target, then scale features."""
    try:
        X = df.drop('target', axis=1)
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    except Exception as e:
        logging.error("Error during preprocessing: %s", e)
        raise

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier and return the trained model."""
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        logging.error("Error training model: %s", e)
        raise

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model and print the classification report and confusion matrix."""
    try:
        predictions = model.predict(X_test)
        print("Classification Report:\n", classification_report(y_test, predictions))
        print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
    except Exception as e:
        logging.error("Error during evaluation: %s", e)
        raise

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    try:
        data = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(data)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        logging.critical("Critical error in the main execution: %s", e)

if __name__ == "__main__":
    main()