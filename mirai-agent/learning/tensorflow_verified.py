"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-15T20:25:24.196878

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

def create_model(input_shape: tuple, num_classes: int) -> keras.Model:
    """
    Creates a simple neural network model.

    Args:
        input_shape (tuple): Shape of the input data.
        num_classes (int): Number of output classes.

    Returns:
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Flatten(input_shape=input_shape),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def load_data() -> tuple:
    """
    Loads the MNIST dataset.

    Returns:
        tuple: Training and testing data and labels.
    """
    try:
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        return (x_train, y_train), (x_test, y_test)
    except Exception as e:
        raise RuntimeError("Failed to load the dataset.") from e

def preprocess_data(x: np.ndarray) -> np.ndarray:
    """
    Preprocesses the input data.

    Args:
        x (np.ndarray): Input data to preprocess.

    Returns:
        np.ndarray: Preprocessed data.
    """
    return x.astype('float32') / 255.0

def train_model(model: keras.Model, x_train: np.ndarray, y_train: np.ndarray, epochs: int) -> None:
    """
    Trains the model on the given data.

    Args:
        model (keras.Model): The compiled Keras model.
        x_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
        epochs (int): Number of training epochs.
    """
    try:
        model.fit(x_train, y_train, epochs=epochs)
    except Exception as e:
        raise RuntimeError("Model training failed.") from e

def main() -> None:
    """
    Main function to run the model training process.
    """
    (x_train, y_train), (x_test, y_test) = load_data()
    x_train = preprocess_data(x_train)
    x_test = preprocess_data(x_test)

    model = create_model(input_shape=(28, 28), num_classes=10)
    train_model(model, x_train, y_train, epochs=5)

    # Evaluate the model
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print(f'Test accuracy: {test_acc:.4f}')

if __name__ == "__main__":
    main()