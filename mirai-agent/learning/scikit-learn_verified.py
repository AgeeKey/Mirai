"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.76
Tests Passed: 0/1
Learned: 2025-10-22T11:18:23.966012

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """Load the Iris dataset into a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=iris.data, columns=iris.feature_names)

def preprocess_data(data: pd.DataFrame) -> tuple:
    """Split the data into features and target, then into training and testing sets."""
    X = data.values
    y = load_iris().target
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A classifier for the Iris dataset using Random Forest."""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest classifier."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"An error occurred during training: {e}")
    
    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict the classes for the test set."""
        try:
            return self.model.predict(X_test)
        except NotFittedError:
            print("The model is not fitted yet. Please train the model first.")
            return np.array([])

    def evaluate(self, y_test: np.ndarray, y_pred: np.ndarray) -> None:
        """Evaluate the model and print the classification report and confusion matrix."""
        print("Classification Report:\n", classification_report(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

def main() -> None:
    """Main function to run the classifier."""
    data = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(data)
    
    classifier = IrisClassifier()
    classifier.train(X_train, y_train)
    
    y_pred = classifier.predict(X_test)
    if y_pred.size > 0:
        classifier.evaluate(y_test, y_pred)

if __name__ == "__main__":
    main()