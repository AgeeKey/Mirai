"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-14T20:10:48.127643

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
    try:
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['target'] = iris.target
        return df
    except Exception as e:
        logging.error("Error loading data: %s", e)
        raise

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the given training data."""
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        logging.error("Error training model: %s", e)
        raise

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model using accuracy score and classification report."""
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        logging.info("Accuracy: %.2f%%", accuracy * 100)
        logging.info("Classification Report:\n%s", classification_report(y_test, predictions))
        logging.info("Confusion Matrix:\n%s", confusion_matrix(y_test, predictions))
    except Exception as e:
        logging.error("Error evaluating model: %s", e)
        raise

def main() -> None:
    """Main function to load data, train and evaluate the model."""
    try:
        # Load dataset
        df = load_data()
        
        # Split the data into features and target variable
        X = df.iloc[:, :-1].values  # Features
        y = df['target'].values      # Target
        
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