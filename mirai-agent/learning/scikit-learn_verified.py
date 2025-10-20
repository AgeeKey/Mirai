"""
scikit-learn - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.96
Tests Passed: 0/1
Learned: 2025-10-20T06:20:55.176354

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris

def main() -> None:
    """
    Main function to load data, train a Random Forest model, and evaluate its performance.
    """
    try:
        # Load the Iris dataset
        iris = load_iris()
        X = iris.data
        y = iris.target

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Standardize the features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Initialize and train the Random Forest Classifier
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()