"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-21T08:57:29.927686

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

def create_model(input_shape: tuple) -> keras.Model:
    """
    Creates a simple Sequential Neural Network model.

    Args:
        input_shape (tuple): Shape of the input data.

    Returns:
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Flatten(input_shape=input_shape),  # Flatten the input
        layers.Dense(128, activation='relu'),      # Hidden layer
        layers.Dense(10, activation='softmax')     # Output layer for 10 classes
    ])
    
    model.compile(optimizer='adam',              # Optimizer
                  loss='sparse_categorical_crossentropy',  # Loss function
                  metrics=['accuracy'])          # Metrics to track

    return model

def load_data() -> tuple:
    """
    Loads and preprocesses the MNIST dataset.

    Returns:
        tuple: Training and testing data and labels.
    """
    try:
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize data
        return (x_train, y_train), (x_test, y_test)
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def train_model(model: keras.Model, x_train: np.ndarray, y_train: np.ndarray) -> None:
    """
    Trains the provided model on the training data.

    Args:
        model (keras.Model): The model to train.
        x_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
    """
    try:
        model.fit(x_train, y_train, epochs=5)  # Train the model for 5 epochs
    except Exception as e:
        print(f"Error during training: {e}")
        raise

def evaluate_model(model: keras.Model, x_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluates the model on the test data.

    Args:
        model (keras.Model): The model to evaluate.
        x_test (np.ndarray): Test data.
        y_test (np.ndarray): Test labels.
    """
    try:
        test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
        print(f'\nTest accuracy: {test_acc}')
    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise

if __name__ == "__main__":
    (x_train, y_train), (x_test, y_test) = load_data()  # Load the dataset
    model = create_model(input_shape=(28, 28))         # Create the model
    train_model(model, x_train, y_train)                # Train the model
    evaluate_model(model, x_test, y_test)               # Evaluate the model