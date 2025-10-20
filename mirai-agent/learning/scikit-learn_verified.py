"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-20T16:45:52.883645

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
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def preprocess_data(data: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Separate features and target variable from the DataFrame."""
    X = data.drop('target', axis=1).values
    y = data['target'].values
    return X, y

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split the dataset into training and testing sets."""
    return train_test_split(X, y, test_size=test_size, random_state=42)

class RandomForestModel:
    """A Random Forest Classifier wrapper for training and prediction."""
    
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
        self.is_fitted = False

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the Random Forest model."""
        try:
            self.model.fit(X, y)
            self.is_fitted = True
        except Exception as e:
            print(f"Error during training: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""
        if not self.is_fitted:
            raise NotFittedError("This RandomForestModel instance is not fitted yet.")
        return self.model.predict(X)

def main() -> None:
    """Main function to execute the machine learning pipeline."""
    data = load_data()
    X, y = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_data(X, y)

    model = RandomForestModel()
    model.train(X_train, y_train)

    try:
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, predictions))
    except NotFittedError as e:
        print(e)

if __name__ == "__main__":
    main()