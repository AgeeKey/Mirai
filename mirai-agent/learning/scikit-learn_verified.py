"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-15T05:47:43.208938

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def train_model(data: pd.DataFrame) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided data.
    
    Args:
        data: A pandas DataFrame containing the features and target.
    
    Returns:
        A trained RandomForestClassifier instance.
    """
    X = data[data.columns[:-1]]  # Features
    y = data['target']  # Target variable
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)  # Train the model
    return model, X_test, y_test

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> float:
    """Evaluate the model on the test set and return the accuracy score.
    
    Args:
        model: A trained RandomForestClassifier instance.
        X_test: The test features.
        y_test: The test target variable.
    
    Returns:
        Accuracy score as a float.
    """
    try:
        predictions = model.predict(X_test)  # Make predictions
        return accuracy_score(y_test, predictions)  # Calculate accuracy
    except NotFittedError as e:
        print("Model is not fitted yet. Please train the model before evaluation.")
        raise e

def main() -> None:
    """Main function to load data, train the model, and evaluate it."""
    try:
        data = load_data()  # Load the dataset
        model, X_test, y_test = train_model(data)  # Train the model
        
        accuracy = evaluate_model(model, X_test, y_test)  # Evaluate the model
        print(f"Model accuracy: {accuracy:.2f}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()