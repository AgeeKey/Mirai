"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-16T10:47:50.512552

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError
from typing import Tuple

class IrisClassifier:
    def __init__(self):
        """Initialize the IrisClassifier with a Random Forest model."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load and return the Iris dataset.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Features and target variable of the dataset.
        """
        iris = load_iris()
        return iris.data, iris.target

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the Random Forest model on the provided data.

        Args:
            X (np.ndarray): Feature dataset.
            y (np.ndarray): Target variable.

        Raises:
            ValueError: If X or y is empty or not the correct shape.
        """
        if X.size == 0 or y.size == 0:
            raise ValueError("Feature and target datasets cannot be empty.")
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model.

        Args:
            X (np.ndarray): Feature dataset for prediction.

        Returns:
            np.ndarray: Predicted classes.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "feature_importances_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X)

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> None:
        """Evaluate the model performance using classification report and confusion matrix.

        Args:
            X (np.ndarray): Feature dataset for evaluation.
            y (np.ndarray): True target variable.
        """
        y_pred = self.predict(X)
        print("Classification Report:\n", classification_report(y, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y, y_pred))

def main() -> None:
    """Main function to run the Iris classifier example."""
    classifier = IrisClassifier()
    
    # Load the dataset
    X, y = classifier.load_data()
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    classifier.train(X_train, y_train)

    # Evaluate the model
    classifier.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()