"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-19T04:35:12.581142

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and convert it to a DataFrame."""
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    return df

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided data.

    Args:
        X (np.ndarray): Features for training.
        y (np.ndarray): Target variable for training.

    Returns:
        RandomForestClassifier: Trained classifier.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)  # Train the model
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model and print the accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (np.ndarray): Test features.
        y_test (np.ndarray): Test target variable.
    """
    try:
        predictions = model.predict(X_test)  # Make predictions
        accuracy = accuracy_score(y_test, predictions)  # Calculate accuracy
        print(f"Accuracy: {accuracy:.2f}")
        print(classification_report(y_test, predictions))  # Print classification report
    except NotFittedError as e:
        print("Model is not fitted yet:", e)

def main() -> None:
    """Main function to execute the training and evaluation of the model."""
    # Load and prepare the data
    df = load_data()
    X = df.drop(columns='target').values  # Features
    y = df['target'].values  # Target variable
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()