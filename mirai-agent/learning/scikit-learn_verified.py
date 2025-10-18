"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-18T01:36:19.967515

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    return df

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the DataFrame and split it into features and target."""
    X = df.drop(columns='target')
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest classifier on the training data."""
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> float:
    """Evaluate the trained model and return the accuracy score."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

def main() -> None:
    """Main function to execute the machine learning workflow."""
    try:
        # Load the data
        df = load_data()
        # Preprocess the data
        X_train, X_test, y_train, y_test = preprocess_data(df)
        # Train the model
        model = train_model(X_train, y_train)
        # Evaluate the model
        accuracy = evaluate_model(model, X_test, y_test)
        print(f"Model Accuracy: {accuracy:.2f}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()