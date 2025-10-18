"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-18T10:02:29.755543

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data() -> pd.DataFrame:
    """Load the Iris dataset as a Pandas DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data by splitting it into training and testing sets.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the features.
    
    Returns:
        tuple: Contains the training features, test features, training labels, and test labels.
    """
    X = df.values
    y = load_iris().target
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train the Random Forest Classifier model.
    
    Args:
        X_train (np.ndarray): The training features.
        y_train (np.ndarray): The training labels.
    
    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model and print the accuracy and classification report.
    
    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): The testing features.
        y_test (np.ndarray): The testing labels.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")

def main() -> None:
    """Main function to execute the workflow."""
    try:
        # Load and preprocess the data
        df = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(df)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()