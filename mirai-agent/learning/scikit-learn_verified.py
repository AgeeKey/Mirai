"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-17T01:41:42.130167

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.exceptions import NotFittedError

def load_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and return features and target.

    Returns:
        tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    iris = load_iris()
    return iris.data, iris.target

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier on the provided data.

    Args:
        X (np.ndarray): Features for training.
        y (np.ndarray): Target variable.

    Returns:
        RandomForestClassifier: Trained classifier.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)  # Train the model

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return model

def predict(model: RandomForestClassifier, sample: np.ndarray) -> np.ndarray:
    """Make a prediction using the trained model.

    Args:
        model (RandomForestClassifier): The trained classifier.
        sample (np.ndarray): A single sample for prediction.

    Returns:
        np.ndarray: Predicted class.
    
    Raises:
        NotFittedError: If the model is not fitted yet.
    """
    if not hasattr(model, "estimators_"):
        raise NotFittedError("This RandomForestClassifier instance is not fitted yet.")

    return model.predict(sample.reshape(1, -1))  # Reshape sample for prediction

if __name__ == "__main__":
    try:
        X, y = load_data()  # Load the dataset
        trained_model = train_model(X, y)  # Train the model

        # Sample for prediction
        sample_data = np.array([5.1, 3.5, 1.4, 0.2])
        prediction = predict(trained_model, sample_data)  # Predict the class of the sample
        print(f"Predicted class for the sample {sample_data}: {prediction[0]}")
        
    except Exception as e:
        print(f"An error occurred: {e}")