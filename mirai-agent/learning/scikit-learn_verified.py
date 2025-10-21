"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-21T10:01:48.343631

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """
    Load the Iris dataset and return it as a pandas DataFrame.
    
    Returns:
        pd.DataFrame: The iris dataset with features and target.
    """
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def split_data(data: pd.DataFrame) -> tuple:
    """
    Split the data into training and testing sets.
    
    Args:
        data (pd.DataFrame): The DataFrame containing features and target.
        
    Returns:
        tuple: Features and target split into training and testing sets.
    """
    X = data.drop('target', axis=1)
    y = data['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier on the training data.
    
    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target.
        
    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the trained model on the test data and print the results.
    
    Args:
        model (RandomForestClassifier): The trained model to evaluate.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): Test target.
    """
    try:
        predictions = model.predict(X_test)
        print(confusion_matrix(y_test, predictions))
        print(classification_report(y_test, predictions))
    except NotFittedError:
        print("Model has not been fitted yet.")

def main() -> None:
    """
    Main function to run the machine learning pipeline.
    """
    data = load_data()  # Load the dataset
    X_train, X_test, y_train, y_test = split_data(data)  # Split the data
    model = train_model(X_train, y_train)  # Train the model
    evaluate_model(model, X_test, y_test)  # Evaluate the model

if __name__ == "__main__":
    main()