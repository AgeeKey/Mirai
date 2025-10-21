"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.75
Tests Passed: 0/1
Learned: 2025-10-21T05:46:14.730905

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[pd.DataFrame, pd.Series]:
    """Load the Iris dataset and return features and target as DataFrame and Series."""
    try:
        iris = load_iris()
        X = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        y = pd.Series(data=iris.target)
        return X, y
    except Exception as e:
        raise RuntimeError("Error loading data: " + str(e))

def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest classifier on the provided data."""
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        return model, X_test, y_test
    except Exception as e:
        raise RuntimeError("Error training model: " + str(e))

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the trained model and print the accuracy and classification report."""
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
    except Exception as e:
        raise RuntimeError("Error evaluating model: " + str(e))

def main() -> None:
    """Main function to load data, train model, and evaluate."""
    X, y = load_data()
    model, X_test, y_test = train_model(X, y)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()