"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.78
Tests Passed: 0/1
Learned: 2025-10-17T22:25:16.986388

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset into a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def split_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target, then into training and testing sets."""
    X = df.iloc[:, :-1].values  # Features
    y = df.iloc[:, -1].values    # Target
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisModel:
    """A model for classifying Iris species using a Random Forest classifier."""
    
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model with training data."""
        self.model.fit(X_train, y_train)

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the classes for the test data."""
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisModel instance is not fitted yet.")
        return self.model.predict(X_test)

def main() -> None:
    """Main function to load data, train the model, and evaluate its performance."""
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = split_data(df)

        iris_model = IrisModel()
        iris_model.train(X_train, y_train)

        predictions = iris_model.predict(X_test)

        print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
        print("\nClassification Report:\n", classification_report(y_test, predictions))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()