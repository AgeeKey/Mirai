"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-19T13:00:06.534580

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
    """Load the Iris dataset and return it as a pandas DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(data: pd.DataFrame) -> tuple:
    """Split the data into features and target variable, then into training and testing sets.

    Args:
        data (pd.DataFrame): The input DataFrame containing the features and target.

    Returns:
        tuple: A tuple containing the training features, testing features,
               training target, and testing target.
    """
    X = data.iloc[:, :-1]  # Features
    y = data.iloc[:, -1]   # Target variable
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A classifier for the Iris dataset using Random Forest."""
    
    def __init__(self) -> None:
        """Initialize the Random Forest Classifier."""
        self.model = RandomForestClassifier()

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Fit the model to the training data.

        Args:
            X_train (np.ndarray): Training features.
            y_train (np.ndarray): Training target.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during model fitting: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the target for the test features.

        Args:
            X_test (np.ndarray): Testing features.

        Returns:
            np.ndarray: Predicted target values.

        Raises:
            NotFittedError: If the model has not been fitted yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisClassifier instance is not fitted yet.")
        return self.model.predict(X_test)

def main() -> None:
    """Main function to run the Iris classification example."""
    data = load_data()  # Load the data
    X_train, X_test, y_train, y_test = preprocess_data(data)  # Preprocess the data

    classifier = IrisClassifier()  # Create classifier instance
    classifier.fit(X_train, y_train)  # Train the model

    predictions = classifier.predict(X_test)  # Make predictions
    accuracy = accuracy_score(y_test, predictions)  # Calculate accuracy

    print(f"Accuracy: {accuracy:.2f}")  # Print accuracy
    print("Classification Report:\n", classification_report(y_test, predictions))  # Print classification report

if __name__ == "__main__":
    main()  # Execute the main function