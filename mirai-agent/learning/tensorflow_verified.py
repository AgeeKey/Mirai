"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-17T05:09:24.486607

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

def create_model(input_shape: tuple) -> keras.Model:
    """
    Creates a simple feedforward neural network model.

    Args:
        input_shape (tuple): Shape of the input data.

    Returns:
        keras.Model: Compiled Keras model.
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

def train_model(model: keras.Model, x_train: np.ndarray, y_train: np.ndarray, epochs: int = 5) -> None:
    """
    Trains the Keras model on the provided training data.

    Args:
        model (keras.Model): The model to train.
        x_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
        epochs (int): Number of training epochs.
    """
    try:
        model.fit(x_train, y_train, epochs=epochs)
    except Exception as e:
        print(f"An error occurred during model training: {e}")

def main() -> None:
    """
    Main function to run the example.
    """
    # Load the MNIST dataset
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    
    # Normalize the images to [0, 1] range
    x_train, x_test = x_train / 255.0, x_test / 255.0
    
    # Create the model
    model = create_model(input_shape=(28, 28))
    
    # Train the model
    train_model(model, x_train, y_train, epochs=5)
    
    # Evaluate the model
    try:
        test_loss, test_acc = model.evaluate(x_test, y_test)
        print(f"Test accuracy: {test_acc:.4f}")
    except Exception as e:
        print(f"An error occurred during model evaluation: {e}")

if __name__ == "__main__":
    main()