"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.78
Tests Passed: 0/1
Learned: 2025-10-15T07:09:15.239118

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the iris dataset and return it as a DataFrame."""
    try:
        data = load_iris()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['target'] = data.target
        return df
    except Exception as e:
        logging.error("Error loading data: %s", e)
        raise

def split_data(df: pd.DataFrame) -> tuple:
    """Split the DataFrame into features and target, then into training and testing sets."""
    try:
        X = df.drop('target', axis=1)
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except KeyError as e:
        logging.error("Target column not found: %s", e)
        raise

class IrisClassifier:
    """A class for training and predicting with a Random Forest classifier on the iris dataset."""
    
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Train the Random Forest model."""
        try:
            self.model.fit(X_train, y_train)
            logging.info("Model trained successfully.")
        except Exception as e:
            logging.error("Error during model training: %s", e)
            raise

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions using the trained model."""
        try:
            return self.model.predict(X)
        except NotFittedError:
            logging.error("Model is not fitted. Please train the model first.")
            raise
        except Exception as e:
            logging.error("Error during prediction: %s", e)
            raise

def main() -> None:
    """Main function to execute the data loading, training, and prediction."""
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = split_data(df)

        classifier = IrisClassifier()
        classifier.train(X_train, y_train)

        predictions = classifier.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        logging.info("Accuracy: %.2f%%", accuracy * 100)
        print(classification_report(y_test, predictions))
    except Exception as e:
        logging.error("An error occurred in the main execution: %s", e)

if __name__ == "__main__":
    main()