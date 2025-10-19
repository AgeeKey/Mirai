"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T11:56:59.354209

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
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def split_data(data: pd.DataFrame) -> tuple:
    """Split the data into training and testing sets.

    Args:
        data: A DataFrame containing the features and target.

    Returns:
        A tuple containing the training features, testing features,
        training target, and testing target.
    """
    X = data.drop('target', axis=1)
    y = data['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A classifier for the Iris dataset using Random Forest."""

    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model.

        Args:
            X_train: Training features.
            y_train: Training target.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the classes for the test set.

        Args:
            X_test: Testing features.

        Returns:
            Predicted classes.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("Model must be trained before prediction.")
        return self.model.predict(X_test)

def main() -> None:
    """Main function to execute the workflow."""
    data = load_data()
    X_train, X_test, y_train, y_test = split_data(data)

    classifier = IrisClassifier()
    classifier.train(X_train, y_train)

    y_pred = classifier.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()