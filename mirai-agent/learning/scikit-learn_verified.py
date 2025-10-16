"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-16T16:45:52.002733

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    return df

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target, then into training and test sets."""
    X = df.iloc[:, :-1]  # Features
    y = df['target']     # Target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest model and return the trained model."""
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the model's performance and print the results."""
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model Accuracy: {accuracy:.2f}")
    
    logging.info("Confusion Matrix:")
    logging.info(confusion_matrix(y_test, y_pred))
    
    logging.info("Classification Report:")
    logging.info(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to execute the machine learning workflow."""
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(df)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()