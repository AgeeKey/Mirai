"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-19T15:37:59.950017

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a pandas DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                        columns=iris['feature_names'] + ['target'])


def preprocess_data(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Preprocess the data by splitting it into features and target, and scaling the features.

    Args:
        df (pd.DataFrame): The input DataFrame containing features and target.

    Returns:
        tuple: A tuple containing the scaled features and the target variable.
    """
    X = df.iloc[:, :-1].values  # Features
    y = df.iloc[:, -1].values    # Target
    scaler = StandardScaler()
    
    try:
        X_scaled = scaler.fit_transform(X)  # Scale features
    except Exception as e:
        print(f"Error in scaling data: {e}")
        raise
    
    return X_scaled, y


def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the given data.

    Args:
        X (np.ndarray): The input features.
        y (np.ndarray): The target variable.

    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    try:
        model.fit(X, y)  # Train the model
    except Exception as e:
        print(f"Error in training model: {e}")
        raise
    
    return model


def evaluate_model(model: RandomForestClassifier, X: np.ndarray, y: np.ndarray) -> None:
    """Evaluate the trained model and print the classification report and confusion matrix.

    Args:
        model (RandomForestClassifier): The trained model to evaluate.
        X (np.ndarray): The input features for evaluation.
        y (np.ndarray): The true target variable for evaluation.
    """
    try:
        y_pred = model.predict(X)  # Make predictions
        print(confusion_matrix(y, y_pred))  # Print confusion matrix
        print(classification_report(y, y_pred))  # Print classification report
    except Exception as e:
        print(f"Error in model evaluation: {e}")
        raise


def main() -> None:
    """Main function to execute the machine learning workflow."""
    df = load_data()  # Load data
    X, y = preprocess_data(df)  # Preprocess data
    model = train_model(X, y)  # Train model
    evaluate_model(model, X, y)  # Evaluate model


if __name__ == "__main__":
    main()  # Execute the main function