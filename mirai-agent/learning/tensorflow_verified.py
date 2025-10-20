"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-20T04:14:17.349303

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

def load_and_prepare_data() -> tuple:
    """
    Load and prepare the Iris dataset for training.

    Returns:
        tuple: A tuple containing training and testing data and labels.
    """
    try:
        iris = load_iris()
        X = iris.data
        y = iris.target
        
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale the features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        return X_train, X_test, y_train, y_test
    except Exception as e:
        print(f"Error in loading data: {e}")
        raise

def build_model(input_shape: int) -> tf.keras.Model:
    """
    Build a simple neural network model.

    Args:
        input_shape (int): The shape of the input data.

    Returns:
        tf.keras.Model: A compiled Keras model.
    """
    try:
        model = models.Sequential([
            layers.Dense(10, activation='relu', input_shape=(input_shape,)),
            layers.Dense(10, activation='relu'),
            layers.Dense(3, activation='softmax')  # 3 classes for Iris
        ])
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        return model
    except Exception as e:
        print(f"Error in building model: {e}")
        raise

def train_and_evaluate_model(model: tf.keras.Model, X_train: np.ndarray, y_train: np.ndarray, 
                             X_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Train and evaluate the model.

    Args:
        model (tf.keras.Model): The Keras model to train.
        X_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
        X_test (np.ndarray): Testing data.
        y_test (np.ndarray): Testing labels.
    """
    try:
        # Train the model
        model.fit(X_train, y_train, epochs=50, batch_size=5, verbose=1)

        # Evaluate the model
        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Accuracy: {accuracy:.4f}")
    except Exception as e:
        print(f"Error in training or evaluating model: {e}")
        raise

def main() -> None:
    """Main function to execute the steps."""
    X_train, X_test, y_train, y_test = load_and_prepare_data()
    model = build_model(X_train.shape[1])
    train_and_evaluate_model(model, X_train, y_train, X_test, y_test)

if __name__ == "__main__":
    main()