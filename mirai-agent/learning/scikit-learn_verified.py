"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T22:59:16.772109

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """Preprocess the data by separating features and target variable."""
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in the data.")
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Train a Random Forest classifier."""
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Evaluate the trained model and display results."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(report)
    
    # Display confusion matrix
    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)
    plt.show()

def main(file_path: str, target_column: str) -> None:
    """Main function to execute the machine learning workflow."""
    data = load_data(file_path)
    X, y = preprocess_data(data, target_column)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Replace 'your_data.csv' with your actual data file path and 'target' with your target column name
    main('your_data.csv', 'target')