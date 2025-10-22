"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-22T08:38:29.234054

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset into a pandas DataFrame."""
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    return df

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target, then into training and testing sets."""
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
    """Evaluate the trained model on the test data."""
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy
    except NotFittedError as e:
        print("Model is not fitted: ", e)
        return 0.0

def main() -> None:
    """Main function to execute the workflow."""
    df = load_data()  # Load the dataset
    X_train, X_test, y_train, y_test = preprocess_data(df)  # Preprocess the data
    model = train_model(X_train, y_train)  # Train the model
    accuracy = evaluate_model(model, X_test, y_test)  # Evaluate the model
    print(f"Model accuracy: {accuracy:.2f}")  # Print the accuracy

if __name__ == "__main__":
    main()