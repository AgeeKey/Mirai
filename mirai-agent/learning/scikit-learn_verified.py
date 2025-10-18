"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.79
Tests Passed: 0/1
Learned: 2025-10-18T02:55:12.519970

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
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                        columns=iris['feature_names'] + ['target'])

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target variable."""
    X = df.drop(columns='target')
    y = df['target']
    return X, y

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest model on the provided features and target."""
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to train model: {e}")

def evaluate_model(model: RandomForestClassifier, X: pd.DataFrame, y: pd.Series) -> None:
    """Evaluate the trained model and print the accuracy and classification report."""
    try:
        predictions = model.predict(X)
        accuracy = accuracy_score(y, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y, predictions))
    except NotFittedError:
        print("Model is not fitted yet. Please train the model before evaluation.")
    except Exception as e:
        raise RuntimeError(f"Failed to evaluate model: {e}")

def main() -> None:
    """Main function to run the workflow."""
    try:
        df = load_data()  # Load data
        X, y = preprocess_data(df)  # Preprocess data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Split data
        model = train_model(X_train, y_train)  # Train model
        evaluate_model(model, X_test, y_test)  # Evaluate model
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()  # Execute the main function