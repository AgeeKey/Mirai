"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-20T22:06:45.845622

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.exceptions import NotFittedError
from sklearn.datasets import load_iris

def load_data() -> pd.DataFrame:
    """Loads the Iris dataset and returns it as a DataFrame."""
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def train_model(data: pd.DataFrame) -> RandomForestClassifier:
    """Trains a Random Forest classifier on the provided DataFrame.
    
    Args:
        data (pd.DataFrame): The input DataFrame containing features and target.
        
    Returns:
        RandomForestClassifier: The trained classifier.
    """
    X = data.drop('target', axis=1)
    y = data['target']

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the classifier
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model accuracy: {accuracy:.2f}")
    print(classification_report(y_test, predictions))

    return model

def make_prediction(model: RandomForestClassifier, sample: np.ndarray) -> int:
    """Makes a prediction using the trained model.
    
    Args:
        model (RandomForestClassifier): The trained classifier.
        sample (np.ndarray): A single sample for prediction.
        
    Returns:
        int: The predicted class label.
        
    Raises:
        NotFittedError: If the model has not been fitted before predicting.
    """
    if not hasattr(model, "estimators_"):
        raise NotFittedError("Model is not fitted yet.")

    prediction = model.predict(sample.reshape(1, -1))
    return prediction[0]

if __name__ == "__main__":
    # Load the data
    data = load_data()

    # Train the model
    model = train_model(data)

    # Example prediction
    sample_input = np.array([5.1, 3.5, 1.4, 0.2])  # Example feature values
    try:
        prediction = make_prediction(model, sample_input)
        print(f"Predicted class: {prediction}")
    except NotFittedError as e:
        print(e)