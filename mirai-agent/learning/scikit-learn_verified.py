"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-15T16:37:20.613435

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_and_prepare_data() -> pd.DataFrame:
    """Loads the Iris dataset and prepares it as a pandas DataFrame."""
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def split_data(data: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Splits the data into training and testing sets.

    Args:
        data (pd.DataFrame): The dataset to split.

    Returns:
        tuple: A tuple containing the training features, test features, training labels, and test labels.
    """
    X = data.drop('target', axis=1).values
    y = data['target'].values
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisModel:
    """A class for training and predicting with the Iris dataset using Random Forest."""
    
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Trains the Random Forest model.

        Args:
            X_train (np.ndarray): The training features.
            y_train (np.ndarray): The training labels.
        """
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Makes predictions using the trained model.

        Args:
            X_test (np.ndarray): The test features.

        Returns:
            np.ndarray: The predicted labels.

        Raises:
            NotFittedError: If the model has not been trained yet.
        """
        if not hasattr(self.model, "estimators_"):
            raise NotFittedError("This IrisModel instance is not fitted yet.")
        return self.model.predict(X_test)

def main() -> None:
    """Main function to run the Iris classification example."""
    # Load and prepare the data
    data = load_and_prepare_data()
    
    # Split the data
    X_train, X_test, y_train, y_test = split_data(data)
    
    # Initialize and train the model
    model = IrisModel()
    model.train(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()