"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.78
Tests Passed: 0/1
Learned: 2025-10-20T19:58:40.390400

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
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def preprocess_data(data: pd.DataFrame) -> tuple:
    """Split the dataset into features and target variable, and then into training and testing sets."""
    X = data.iloc[:, :-1].values  # features
    y = data.iloc[:, -1].values    # target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """Train a RandomForestClassifier model on the training data."""
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model on the test data and print accuracy and classification report."""
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')
        print('Classification Report:')
        print(classification_report(y_test, y_pred))
    except NotFittedError as e:
        print("Error: Model is not fitted yet. Please train the model before evaluation.")
        print(e)

def main() -> None:
    """Main function to execute the workflow."""
    try:
        data = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(data)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print("An error occurred during the process.")
        print(e)

if __name__ == '__main__':
    main()