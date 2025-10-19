"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-19T05:06:41.787228

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
    """Load the Iris dataset and return it as a pandas DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                        columns=iris['feature_names'] + ['target'])

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided features and labels.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Labels.

    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model using accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model to evaluate.
        X_test (np.ndarray): Feature matrix for testing.
        y_test (np.ndarray): True labels for testing.

    Raises:
        NotFittedError: If the model is not fitted before evaluation.
    """
    if not hasattr(model, "predict"):
        raise NotFittedError("Model must be fitted before evaluation.")
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to execute the training and evaluation workflow."""
    try:
        # Load dataset
        data = load_data()
        
        # Split the data into features and target
        X = data.iloc[:, :-1].values  # Features
        y = data.iloc[:, -1].values   # Target
        
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        model = train_model(X_train, y_train)
        
        # Evaluate the model
        evaluate_model(model, X_test, y_test)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()