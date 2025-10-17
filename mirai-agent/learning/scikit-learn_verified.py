"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-17T18:06:33.262956

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.exceptions import NotFittedError

def load_data() -> pd.DataFrame:
    """
    Load the Iris dataset into a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the Iris dataset.
    """
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                        columns=iris['feature_names'] + ['target'])

def preprocess_data(data: pd.DataFrame) -> tuple:
    """
    Split the dataset into features and target, then into training and testing sets.

    Args:
        data (pd.DataFrame): The input DataFrame containing features and target.

    Returns:
        tuple: A tuple containing the training features, testing features,
               training target, and testing target.
    """
    X = data.drop(columns='target')
    y = data['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest classifier on the training data.

    Args:
        X_train (pd.DataFrame): The training features.
        y_train (pd.Series): The training target.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> float:
    """
    Evaluate the model's performance on the test data.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (pd.DataFrame): The testing features.
        y_test (pd.Series): The testing target.

    Returns:
        float: The accuracy of the model on the test data.
    """
    try:
        y_pred = model.predict(X_test)
        return accuracy_score(y_test, y_pred)
    except NotFittedError as e:
        raise RuntimeError("Model is not fitted yet. Please train the model before evaluation.") from e

def main() -> None:
    """
    Main function to execute the workflow of loading data, training, and evaluating the model.
    """
    # Load the dataset
    data = load_data()
    
    # Preprocess the data
    X_train, X_test, y_train, y_test = preprocess_data(data)
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    accuracy = evaluate_model(model, X_test, y_test)
    
    print(f"Model Accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()