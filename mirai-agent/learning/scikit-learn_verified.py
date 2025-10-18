"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.77
Tests Passed: 0/1
Learned: 2025-10-18T04:14:25.455494

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_data() -> pd.DataFrame:
    """Load the Iris dataset and return it as a DataFrame."""
    try:
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['target'] = iris.target
        return df
    except Exception as e:
        logging.error("Error loading data: %s", e)
        raise

def preprocess_data(df: pd.DataFrame) -> tuple:
    """Preprocess the DataFrame and split it into train and test sets."""
    try:
        X = df.drop('target', axis=1)
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.error("Error during preprocessing: %s", e)
        raise

class IrisClassifier:
    """A simple classifier for the Iris dataset using Random Forest."""

    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the Random Forest model."""
        try:
            self.model.fit(X_train, y_train)
            logging.info("Model training completed.")
        except Exception as e:
            logging.error("Error during training: %s", e)
            raise

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict class labels for the provided data."""
        try:
            if not hasattr(self.model, 'estimators_'):
                raise NotFittedError("This IrisClassifier instance is not fitted yet.")
            return self.model.predict(X_test)
        except NotFittedError as e:
            logging.error("Model not fitted: %s", e)
            raise
        except Exception as e:
            logging.error("Error during prediction: %s", e)
            raise

def main() -> None:
    """Main function to execute the workflow."""
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(df)
        
        classifier = IrisClassifier()
        classifier.train(X_train, y_train)
        
        predictions = classifier.predict(X_test)
        
        accuracy = accuracy_score(y_test, predictions)
        logging.info("Accuracy: %.2f%%", accuracy * 100)
        
        report = classification_report(y_test, predictions)
        logging.info("Classification Report:\n%s", report)
        
    except Exception as e:
        logging.error("An error occurred in the main function: %s", e)

if __name__ == "__main__":
    main()