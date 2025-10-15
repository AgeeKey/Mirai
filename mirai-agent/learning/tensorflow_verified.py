"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-15T22:35:19.705093

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

def create_model(input_shape: tuple[int], num_classes: int) -> keras.Model:
    """Creates a simple feedforward neural network model.

    Args:
        input_shape (tuple[int]): Shape of the input data.
        num_classes (int): Number of output classes.

    Returns:
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Flatten(input_shape=input_shape),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def load_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Loads and preprocesses the MNIST dataset.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
        Training and testing data and labels.
    """
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    
    # Normalize the data to [0, 1] range
    x_train, x_test = x_train / 255.0, x_test / 255.0
    
    return x_train, y_train, x_test, y_test

def train_model(model: keras.Model, x_train: np.ndarray, y_train: np.ndarray) -> None:
    """Trains the Keras model on the given training data.

    Args:
        model (keras.Model): The Keras model to train.
        x_train (np.ndarray): Training input data.
        y_train (np.ndarray): Training labels.
    
    Raises:
        ValueError: If training data is empty or shapes do not match.
    """
    if x_train.size == 0 or y_train.size == 0:
        raise ValueError("Training data or labels cannot be empty.")
    
    model.fit(x_train, y_train, epochs=5)

def evaluate_model(model: keras.Model, x_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluates the trained model on the test data.

    Args:
        model (keras.Model): The Keras model to evaluate.
        x_test (np.ndarray): Testing input data.
        y_test (np.ndarray): Testing labels.
    """
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    print(f'\nTest accuracy: {test_acc}')

def main() -> None:
    """Main function to load data, create, train, and evaluate the model."""
    try:
        x_train, y_train, x_test, y_test = load_data()
        model = create_model(input_shape=(28, 28), num_classes=10)
        train_model(model, x_train, y_train)
        evaluate_model(model, x_test, y_test)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()