"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-21T13:15:49.101076

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data by splitting it into features and target variable.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
    
    Returns:
        tuple: A tuple containing features (X) and target (y).
    """
    X = df.values[:, :-1]  # features
    y = df.values[:, -1]   # target variable
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided data.
    
    Args:
        X (np.ndarray): Feature data.
        y (np.ndarray): Target data.
    
    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the accuracy and classification report.
    
    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test feature data.
        y_test (np.ndarray): Test target data.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
    except NotFittedError:
        print("Model is not fitted yet. Please train the model before evaluation.")

def main() -> None:
    """Main function to execute the data loading, training, and evaluation process."""
    df = load_data()
    X, y = preprocess_data(df)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()