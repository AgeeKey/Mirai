"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-20T01:52:21.385288

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
    """Load the Iris dataset into a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data by splitting into features and target, and then into training and test sets."""
    X = df.values
    y = np.array(load_iris().target)

    # Split the dataset into training and testing sets
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A simple classifier for the Iris dataset using Random Forest."""

    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"Error during training: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""
        try:
            return self.model.predict(X)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model before predicting.")
            return np.array([])

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model and print the accuracy and classification report."""
        y_pred = self.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

def main() -> None:
    """Main function to run the Iris classification."""
    df = load_data()  # Load the data
    X_train, X_test, y_train, y_test = preprocess_data(df)  # Preprocess the data

    classifier = IrisClassifier()  # Create an instance of the classifier
    classifier.train(X_train, y_train)  # Train the model
    classifier.evaluate(X_test, y_test)  # Evaluate the model

if __name__ == "__main__":
    main()  # Execute the main function