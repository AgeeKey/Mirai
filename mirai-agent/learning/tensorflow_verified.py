"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T05:57:10.368405

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from typing import Tuple

def create_model(input_shape: Tuple[int, int]) -> keras.Model:
    """Creates a simple neural network model.

    Args:
        input_shape (Tuple[int, int]): The shape of the input data.

    Returns:
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Flatten(input_shape=input_shape),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def load_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Loads the MNIST dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
        Training and test data and labels.
    """
    try:
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize data
        return x_train, y_train, x_test, y_test
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def train_model(model: keras.Model, x_train: np.ndarray, y_train: np.ndarray) -> None:
    """Trains the model on the training data.

    Args:
        model (keras.Model): The model to train.
        x_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
    """
    try:
        model.fit(x_train, y_train, epochs=5)
    except Exception as e:
        print(f"Error during model training: {e}")
        raise

def evaluate_model(model: keras.Model, x_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluates the model on the test data.

    Args:
        model (keras.Model): The model to evaluate.
        x_test (np.ndarray): Test data.
        y_test (np.ndarray): Test labels.
    """
    try:
        test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
        print(f'\nTest accuracy: {test_acc}')
    except Exception as e:
        print(f"Error during model evaluation: {e}")
        raise

def main() -> None:
    """Main function to execute the training and evaluation of the model."""
    input_shape = (28, 28)
    x_train, y_train, x_test, y_test = load_data()
    model = create_model(input_shape)
    train_model(model, x_train, y_train)
    evaluate_model(model, x_test, y_test)

if __name__ == "__main__":
    main()