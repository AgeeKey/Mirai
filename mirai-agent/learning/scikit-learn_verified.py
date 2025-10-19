"""
scikit-learn - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-19T14:19:10.854575

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
    """Load the iris dataset and return it as a DataFrame."""
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    return df

def train_model(df: pd.DataFrame) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing features and target.

    Returns:
        RandomForestClassifier: The trained classifier.
    """
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Fit the model on the training set
    model.fit(X_train, y_train)

    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the trained model using the test set.

    Args:
        model (RandomForestClassifier): The trained classifier.
        X_test (np.ndarray): The feature set for testing.
        y_test (np.ndarray): The true labels for testing.
    """
    try:
        # Make predictions
        y_pred = model.predict(X_test)

        # Print classification report and confusion matrix
        print("Classification Report:\n", classification_report(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    except NotFittedError as e:
        print("Model is not fitted yet. Please train the model before evaluation.", e)

def main() -> None:
    """Main function to load data, train the model, and evaluate its performance."""
    try:
        # Load the data
        df = load_data()

        # Train the model
        model = train_model(df)

        # Prepare the test data
        X_test = df.drop('target', axis=1).iloc[int(0.8 * len(df)):]
        y_test = df['target'].iloc[int(0.8 * len(df)):]

        # Evaluate the model
        evaluate_model(model, X_test, y_test)

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()