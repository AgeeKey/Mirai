"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-19T09:51:04.950305

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    try:
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['target'] = iris.target
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def split_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into training and testing sets."""
    try:
        X = df.drop('target', axis=1)
        y = df['target']
        return train_test_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        raise RuntimeError(f"Error splitting data: {e}")

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier model."""
    try:
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise RuntimeError(f"Error training model: {e}")

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model and print accuracy and classification report."""
    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        conf_matrix = confusion_matrix(y_test, predictions)

        print(f"Accuracy: {accuracy:.2f}")
        print("Confusion Matrix:\n", conf_matrix)
        print("Classification Report:\n", classification_report(y_test, predictions))
    except Exception as e:
        raise RuntimeError(f"Error evaluating model: {e}")

def main() -> None:
    """Main function to execute the workflow."""
    df = load_data()
    X_train, X_test, y_train, y_test = split_data(df)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()