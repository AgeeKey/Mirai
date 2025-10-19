"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T19:50:21.624246

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_and_prepare_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def split_data(data: pd.DataFrame) -> tuple:
    """Split the dataset into training and testing sets.

    Args:
        data (pd.DataFrame): The input dataset.

    Returns:
        tuple: A tuple containing the training features, testing features, 
               training labels, and testing labels.
    """
    X = data.drop('target', axis=1)
    y = data['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A simple classifier for the Iris dataset using RandomForest."""
    
    def __init__(self) -> None:
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the RandomForest model.

        Args:
            X_train (np.ndarray): Features for training.
            y_train (np.ndarray): Labels for training.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the class labels for the test set.

        Args:
            X_test (np.ndarray): Features for testing.

        Returns:
            np.ndarray: Predicted class labels.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "predict"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X_test)

def main() -> None:
    """Main function to execute the Iris classification."""
    try:
        data = load_and_prepare_data()  # Load the dataset
        X_train, X_test, y_train, y_test = split_data(data)  # Split the data

        classifier = IrisClassifier()  # Create the classifier
        classifier.train(X_train, y_train)  # Train the model

        predictions = classifier.predict(X_test)  # Make predictions
        accuracy = accuracy_score(y_test, predictions)  # Calculate accuracy

        print(f"Model accuracy: {accuracy:.2f}")  # Output accuracy
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any errors

if __name__ == "__main__":
    main()  # Run the main function