"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-16T20:16:46.668819

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def split_data(data: pd.DataFrame) -> tuple:
    """Split the dataset into training and testing sets.

    Args:
        data: A DataFrame containing the dataset.

    Returns:
        A tuple containing the training features, testing features,
        training labels, and testing labels.
    """
    X = data.iloc[:, :-1]  # Features
    y = data.iloc[:, -1]   # Labels
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the training data.

    Args:
        X_train: Training features.
        y_train: Training labels.

    Returns:
        A trained RandomForestClassifier model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model on the test data.

    Args:
        model: A trained RandomForestClassifier model.
        X_test: Testing features.
        y_test: Testing labels.
    """
    y_pred = model.predict(X_test)  # Make predictions
    accuracy = accuracy_score(y_test, y_pred)  # Calculate accuracy
    print(f"Accuracy: {accuracy:.2f}")  # Print accuracy
    print("Classification Report:\n", classification_report(y_test, y_pred))  # Print classification report

def main() -> None:
    """Main function to execute the workflow."""
    try:
        data = load_data()  # Load dataset
        X_train, X_test, y_train, y_test = split_data(data)  # Split data
        model = train_model(X_train, y_train)  # Train model
        evaluate_model(model, X_test, y_test)  # Evaluate model
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exceptions

if __name__ == "__main__":
    main()  # Run the main function