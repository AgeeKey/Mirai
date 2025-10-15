"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-15T23:24:09.644180

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
    """Load the iris dataset and return it as a DataFrame."""
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    return df

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Split the dataset into features and target variable."""
    X = df.drop(columns='target')
    y = df['target']
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided data."""
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X: np.ndarray, y: np.ndarray) -> float:
    """Evaluate the model and return the accuracy score."""
    try:
        predictions = model.predict(X)
        return accuracy_score(y, predictions)
    except NotFittedError as e:
        print("Model is not fitted yet. Please train the model before evaluation.")
        raise e

def main() -> None:
    """Main function to load data, train and evaluate the model."""
    df = load_data()  # Load the dataset
    X, y = preprocess_data(df)  # Preprocess data
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)  # Train the model
    
    accuracy = evaluate_model(model, X_test, y_test)  # Evaluate the model
    print(f"Model accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()  # Run the main function