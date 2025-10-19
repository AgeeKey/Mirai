"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-19T18:47:11.374422

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
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    return df

def split_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target, then into training and testing sets."""
    X = df.iloc[:, :-1]  # Features
    y = df['target']  # Target variable
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A simple Iris Classifier using Random Forest."""

    def __init__(self) -> None:
        """Initialize the classifier."""
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model with the training data."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the class labels for the test data."""
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])

def evaluate_model(y_test: np.ndarray, predictions: np.ndarray) -> None:
    """Evaluate the model's predictions and print the results."""
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, predictions))

def main() -> None:
    """Main function to execute the workflow."""
    df = load_data()  # Load the dataset
    X_train, X_test, y_train, y_test = split_data(df)  # Split the data

    classifier = IrisClassifier()  # Create a classifier instance
    classifier.train(X_train, y_train)  # Train the model

    predictions = classifier.predict(X_test)  # Make predictions
    evaluate_model(y_test, predictions)  # Evaluate and print results

if __name__ == "__main__":
    main()  # Run the main function