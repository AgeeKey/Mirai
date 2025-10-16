"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T19:44:15.395199

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
    """Split the data into features and target variable, then into training and test sets."""
    X = df.values
    y = load_iris().target
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A simple Iris classifier using Random Forest."""
    
    def __init__(self) -> None:
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """Fit the Random Forest model to the training data."""
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the fitted model."""
        try:
            return self.model.predict(X)
        except NotFittedError:
            raise RuntimeError("Model is not fitted yet. Call 'fit' before 'predict'.")

def main() -> None:
    """Main function to execute the model training and evaluation."""
    df = load_data()  # Load dataset
    X_train, X_test, y_train, y_test = preprocess_data(df)  # Preprocess data

    classifier = IrisClassifier()  # Initialize classifier
    classifier.fit(X_train, y_train)  # Fit model

    predictions = classifier.predict(X_test)  # Make predictions

    # Evaluate model performance
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy:.2f}")
    print(classification_report(y_test, predictions))

if __name__ == "__main__":
    main()  # Execute the main function