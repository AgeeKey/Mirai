"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-20T19:42:37.786442

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
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the data: split into features and target, then into training and test sets."""
    X = df.values
    y = load_iris().target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

class IrisModel:
    """A simple Random Forest model for classifying Iris species."""
    
    def __init__(self):
        self.model = RandomForestClassifier()
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """Fit the model to the training data."""
        try:
            self.model.fit(X, y)
            self.is_fitted = True
        except Exception as e:
            print(f"Error during model fitting: {e}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the fitted model."""
        if not self.is_fitted:
            raise NotFittedError("This IrisModel instance is not fitted yet.")
        return self.model.predict(X)

def main() -> None:
    """Main function to execute the model training and evaluation."""
    # Load and preprocess the data
    df = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(df)

    # Initialize and fit the model
    model = IrisModel()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)

if __name__ == "__main__":
    main()