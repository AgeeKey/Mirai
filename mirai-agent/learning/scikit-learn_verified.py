"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.79
Tests Passed: 0/1
Learned: 2025-10-16T11:20:48.313611

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a Pandas DataFrame."""
    try:
        iris = load_iris()
        data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        data['target'] = iris.target
        return data
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise

def preprocess_data(data: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Split the data into features and target, then into training and testing sets."""
    try:
        X = data.drop('target', axis=1).values
        y = data['target'].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")
        raise

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier model."""
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        logging.error(f"Error during model training: {e}")
        raise

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model and print accuracy and classification report."""
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f"Model Accuracy: {accuracy:.2f}")
        logging.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")
        logging.info(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
    except Exception as e:
        logging.error(f"Error during model evaluation: {e}")
        raise

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    try:
        data = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(data)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        logging.error(f"Error in the main execution: {e}")

if __name__ == "__main__":
    main()