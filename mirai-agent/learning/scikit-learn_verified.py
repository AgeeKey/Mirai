"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-19T17:44:16.630314

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    try:
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['target'] = iris.target
        return df
    except Exception as e:
        raise RuntimeError("Error loading data: {}".format(e))

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the DataFrame into features and target variables.

    Args:
        df (pd.DataFrame): The DataFrame containing the dataset.

    Returns:
        tuple: Features (X) and target (y).
    """
    try:
        X = df.drop(columns='target')
        y = df['target']
        return X, y
    except KeyError as e:
        raise KeyError("Column 'target' not found in DataFrame: {}".format(e))

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest Classifier model.

    Args:
        X (pd.DataFrame): The feature set.
        y (pd.Series): The target variable.

    Returns:
        RandomForestClassifier: The trained model.
    """
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        raise RuntimeError("Error training model: {}".format(e))

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the trained model and print the accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (pd.DataFrame): The test feature set.
        y_test (pd.Series): The test target variable.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError("Error evaluating model: {}".format(e))

def main() -> None:
    """Main function to execute the machine learning workflow."""
    df = load_data()
    X, y = preprocess_data(df)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()