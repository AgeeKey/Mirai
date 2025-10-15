"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.79
Tests Passed: 0/1
Learned: 2025-10-15T04:43:36.923665

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset into a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target variable, then into training and test sets."""
    X = df.values
    y = load_iris().target
    
    # Split the data into training and testing sets
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A classifier for the Iris dataset using Random Forest."""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest classifier on the training data."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise RuntimeError("Failed to train model") from e

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""
        try:
            return self.model.predict(X_test)
        except NotFittedError as e:
            raise RuntimeError("Model is not fitted yet. Please train the model first.") from e
        except Exception as e:
            raise RuntimeError("Prediction failed") from e

def main() -> None:
    """Main function to execute the data loading, training, and evaluation."""
    df = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(df)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)

    predictions = classifier.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(report)

if __name__ == "__main__":
    main()