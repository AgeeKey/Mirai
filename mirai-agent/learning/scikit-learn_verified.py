"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-21T15:09:23.848515

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Loaded dataset.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise FileNotFoundError(f"Error loading file: {e}")

def preprocess_data(data: pd.DataFrame) -> (np.ndarray, np.ndarray):
    """Preprocess the dataset.
    
    Args:
        data (pd.DataFrame): Raw data.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and target arrays.
    """
    # Assuming last column is the target variable
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    return X, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest Classifier model.
    
    Args:
        X (np.ndarray): Feature data.
        y (np.ndarray): Target data.
    
    Returns:
        RandomForestClassifier: Trained model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model performance.
    
    Args:
        model (RandomForestClassifier): Trained model.
        X_test (np.ndarray): Test feature data.
        y_test (np.ndarray): Test target data.
    """
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)

def main(file_path: str) -> None:
    """Main function to load data, train and evaluate the model.
    
    Args:
        file_path (str): Path to the dataset CSV file.
    """
    data = load_data(file_path)
    X, y = preprocess_data(data)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Replace 'your_dataset.csv' with your actual dataset path
    main('your_dataset.csv')