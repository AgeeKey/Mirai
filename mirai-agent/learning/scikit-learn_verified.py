"""
scikit-learn - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-21T20:19:26.779326

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from typing import Tuple

def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load the Iris dataset and return features and labels.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Features and labels of the Iris dataset.
    """
    iris = load_iris()
    return iris.data, iris.target

def split_data(features: np.ndarray, labels: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the dataset into training and testing sets.

    Args:
        features (np.ndarray): Feature data.
        labels (np.ndarray): Labels corresponding to features.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training features, testing features, training labels, testing labels.
    """
    return train_test_split(features, labels, test_size=test_size, random_state=random_state)

def train_model(train_features: np.ndarray, train_labels: np.ndarray) -> RandomForestClassifier:
    """
    Train a Random Forest Classifier model.

    Args:
        train_features (np.ndarray): Training features.
        train_labels (np.ndarray): Training labels.

    Returns:
        RandomForestClassifier: A trained Random Forest model.
    """
    model = RandomForestClassifier()
    model.fit(train_features, train_labels)
    return model

def evaluate_model(model: RandomForestClassifier, test_features: np.ndarray, test_labels: np.ndarray) -> None:
    """
    Evaluate the trained model and print the accuracy and classification report.

    Args:
        model (RandomForestClassifier): The trained model to evaluate.
        test_features (np.ndarray): Testing features.
        test_labels (np.ndarray): Testing labels.
    """
    try:
        predictions = model.predict(test_features)
        accuracy = accuracy_score(test_labels, predictions)
        report = classification_report(test_labels, predictions)
        print(f"Accuracy: {accuracy:.2f}")
        print("Classification Report:\n", report)
    except Exception as e:
        print(f"An error occurred during model evaluation: {e}")

def main() -> None:
    """
    Main function to load data, train the model, and evaluate it.
    """
    features, labels = load_data()
    train_features, test_features, train_labels, test_labels = split_data(features, labels)

    model = train_model(train_features, train_labels)
    evaluate_model(model, test_features, test_labels)

if __name__ == "__main__":
    main()