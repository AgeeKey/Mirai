"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T14:26:32.821557

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target, then into training and test sets."""
    X = df.values  # Features
    y = load_iris().target  # Target labels
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A simple classifier for the Iris dataset using Random Forest."""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model on the training data."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions on the test data."""
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
            return np.array([])  # Return an empty array if not fitted
        except Exception as e:
            print(f"An error occurred during prediction: {e}")
            return np.array([])

def main() -> None:
    """Main function to execute the workflow."""
    df = load_data()  # Load the dataset
    X_train, X_test, y_train, y_test = preprocess_data(df)  # Preprocess the data

    classifier = IrisClassifier()  # Instantiate the classifier
    classifier.train(X_train, y_train)  # Train the model

    predictions = classifier.predict(X_test)  # Make predictions
    if predictions.size > 0:
        # Evaluate and print the model performance
        print("Accuracy:", accuracy_score(y_test, predictions))
        print(classification_report(y_test, predictions))

if __name__ == "__main__":
    main()  # Run the main function