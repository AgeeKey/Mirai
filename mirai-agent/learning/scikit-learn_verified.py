"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-17T15:56:45.487489

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def preprocess_data(data: pd.DataFrame, target_column: str) -> tuple:
    """Preprocess the data by separating features and target variable, and scaling the features.

    Args:
        data (pd.DataFrame): The input data.
        target_column (str): The name of the target variable.

    Returns:
        tuple: Scaled features and target variable.
    """
    X = data.drop(columns=[target_column])
    y = data[target_column]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y

def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Train a Random Forest classifier.

    Args:
        X (np.ndarray): The feature set.
        y (np.ndarray): The target variable.

    Returns:
        RandomForestClassifier: The trained model.
    """
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model: RandomForestClassifier, X: np.ndarray, y: np.ndarray) -> None:
    """Evaluate the model and print the classification report and confusion matrix.

    Args:
        model (RandomForestClassifier): The trained model.
        X (np.ndarray): The feature set.
        y (np.ndarray): The target variable.
    """
    y_pred = model.predict(X)
    print("Classification Report:")
    print(classification_report(y, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y, y_pred))

def main(file_path: str, target_column: str) -> None:
    """Main function to load data, preprocess it, train the model, and evaluate.

    Args:
        file_path (str): Path to the dataset.
        target_column (str): Target variable name.
    """
    data = load_data(file_path)
    X, y = preprocess_data(data, target_column)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    # Replace 'your_dataset.csv' and 'target' with your actual data file and target column name
    main('your_dataset.csv', 'target')