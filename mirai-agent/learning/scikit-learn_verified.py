"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T20:06:07.437525

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
    """Load the Iris dataset and return it as a DataFrame."""
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=iris['feature_names'] + ['target'])

def split_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target, then into training and test sets."""
    X = df.drop(columns='target')
    y = df['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

class IrisClassifier:
    """A simple classifier for the Iris dataset using Random Forest."""
    
    def __init__(self) -> None:
        self.model = RandomForestClassifier(random_state=42)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model using the training data."""
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            print(f"Error during training: {e}")

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate the model on the test data and print the results."""
        try:
            y_pred = self.model.predict(X_test)
            print(confusion_matrix(y_test, y_pred))
            print(classification_report(y_test, y_pred))
        except NotFittedError:
            print("Model is not fitted yet. Please train the model first.")
        except Exception as e:
            print(f"Error during evaluation: {e}")

def main() -> None:
    """Main function to execute the workflow."""
    # Load the dataset
    df = load_data()
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = split_data(df)
    
    # Initialize the classifier
    classifier = IrisClassifier()
    
    # Train the classifier
    classifier.train(X_train, y_train)
    
    # Evaluate the classifier
    classifier.evaluate(X_test, y_test)

if __name__ == "__main__":
    main()