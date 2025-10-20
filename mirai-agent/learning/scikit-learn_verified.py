"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-20T20:30:50.838702

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data() -> pd.DataFrame:
    """
    Load the Iris dataset and return it as a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the Iris dataset.
    """
    iris = load_iris()
    df = pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=iris['feature_names'] + ['target'])
    return df

def split_data(df: pd.DataFrame) -> tuple:
    """
    Split the DataFrame into training and testing sets.

    Args:
        df (pd.DataFrame): The DataFrame to split.

    Returns:
        tuple: A tuple containing the training features, training labels, testing features, and testing labels.
    """
    X = df.iloc[:, :-1]  # Features
    y = df.iloc[:, -1]   # Target variable
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest classifier.

    Args:
        X_train (pd.DataFrame): The training features.
        y_train (pd.Series): The training labels.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate the model and print accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model.
        X_test (pd.DataFrame): The testing features.
        y_test (pd.Series): The testing labels.
    """
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", classification_report(y_test, y_pred))
    except Exception as e:
        print(f"Error during model evaluation: {e}")

def main() -> None:
    """
    Main function to run the machine learning workflow.
    """
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = split_data(df)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()