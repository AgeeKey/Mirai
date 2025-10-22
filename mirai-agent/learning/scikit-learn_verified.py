"""
scikit-learn - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-22T12:07:23.828476

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.datasets import load_iris

def load_data() -> pd.DataFrame:
    """
    Load the Iris dataset and return it as a pandas DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame containing the Iris dataset.
    """
    iris = load_iris()
    return pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                        columns=iris['feature_names'] + ['target'])

def preprocess_data(df: pd.DataFrame) -> tuple:
    """
    Preprocess the dataset by splitting it into features and target variables,
    and then into training and testing sets.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the data.
    
    Returns:
        tuple: A tuple containing training and testing features and targets.
    """
    X = df.iloc[:, :-1]  # Features
    y = df.iloc[:, -1]   # Target variable
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> LogisticRegression:
    """
    Train a Logistic Regression model on the training data.
    
    Args:
        X_train (np.ndarray): Training features.
        y_train (np.ndarray): Training target variable.
    
    Returns:
        LogisticRegression: The trained logistic regression model.
    """
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: LogisticRegression, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the model on the test data and print the accuracy, confusion matrix, 
    and classification report.
    
    Args:
        model (LogisticRegression): The trained model.
        X_test (np.ndarray): Testing features.
        y_test (np.ndarray): Testing target variable.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    print(f'Accuracy: {accuracy:.2f}')
    print('Confusion Matrix:\n', conf_matrix)
    print('Classification Report:\n', classification_report(y_test, y_pred))

def main() -> None:
    """
    Main function to execute the data loading, preprocessing, model training, 
    and evaluation.
    """
    try:
        df = load_data()
        X_train, X_test, y_train, y_test = preprocess_data(df)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    main()