"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-18T23:35:33.842175

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.exceptions import NotFittedError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class IrisClassifier:
    """A classifier for the Iris dataset using a Random Forest model."""

    def __init__(self) -> None:
        """Initialize the classifier with a Random Forest model."""
        self.model = RandomForestClassifier(random_state=42)
        self.is_fitted = False

    def load_data(self) -> pd.DataFrame:
        """Load the Iris dataset.

        Returns:
            pd.DataFrame: A DataFrame containing the Iris dataset.
        """
        iris = load_iris()
        return pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                            columns=iris['feature_names'] + ['target'])

    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Train the Random Forest model.

        Args:
            X (pd.DataFrame): The input features.
            y (pd.Series): The target labels.

        Raises:
            ValueError: If X and y have incompatible shapes.
        """
        if X.shape[0] != y.shape[0]:
            raise ValueError("The number of samples in X and y must match.")
        
        self.model.fit(X, y)
        self.is_fitted = True
        logging.info("Model trained successfully.")

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions using the trained model.

        Args:
            X (pd.DataFrame): The input features.

        Returns:
            np.ndarray: The predicted labels.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not self.is_fitted:
            raise NotFittedError("The model must be trained before making predictions.")
        
        return self.model.predict(X)

    def evaluate(self, y_true: pd.Series, y_pred: np.ndarray) -> None:
        """Evaluate the model's performance.

        Args:
            y_true (pd.Series): The true labels.
            y_pred (np.ndarray): The predicted labels.
        """
        accuracy = accuracy_score(y_true, y_pred)
        logging.info(f"Accuracy: {accuracy:.4f}")
        logging.info(f"Confusion Matrix:\n{confusion_matrix(y_true, y_pred)}")
        logging.info(f"Classification Report:\n{classification_report(y_true, y_pred)}")

def main() -> None:
    """Main function to run the Iris classifier."""
    iris_classifier = IrisClassifier()
    
    # Load data
    data = iris_classifier.load_data()
    X = data.iloc[:, :-1]  # Features
    y = data.iloc[:, -1]   # Target
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    iris_classifier.train(X_train, y_train)
    
    # Make predictions
    y_pred = iris_classifier.predict(X_test)
    
    # Evaluate the model
    iris_classifier.evaluate(y_test, y_pred)

if __name__ == "__main__":
    main()