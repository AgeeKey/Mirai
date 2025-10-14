"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-14T16:56:03.127746

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris

def load_and_prepare_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a pandas DataFrame."""
    try:
        iris = load_iris()
        data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        data['target'] = iris.target
        return data
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided features and target.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.

    Returns:
        RandomForestClassifier: Trained model.
    """
    try:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model using accuracy and classification report.

    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Test feature matrix.
        y_test (np.ndarray): Test target vector.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)
    except Exception as e:
        raise RuntimeError(f"Error evaluating model: {e}")

def main() -> None:
    """Main function to execute the machine learning workflow."""
    try:
        # Load and prepare data
        data = load_and_prepare_data()
        
        # Split data into features and target
        X = data.iloc[:, :-1].values  # Features
        y = data['target'].values      # Target

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = train_model(X_train, y_train)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()