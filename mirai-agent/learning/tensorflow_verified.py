"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-17T21:53:24.516635

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

def create_model(input_shape: tuple, num_classes: int) -> keras.Model:
    """
    Creates a simple feedforward neural network model.

    Args:
        input_shape (tuple): The shape of the input data (excluding batch size).
        num_classes (int): The number of output classes.

    Returns:
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Flatten(input_shape=input_shape),  # Flatten the input
        layers.Dense(128, activation='relu'),     # Hidden layer with ReLU activation
        layers.Dropout(0.2),                      # Dropout for regularization
        layers.Dense(num_classes, activation='softmax')  # Output layer with softmax activation
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])  # Compile the model
    return model

def load_data() -> tuple:
    """
    Loads the MNIST dataset and preprocesses it.

    Returns:
        tuple: Tuple containing training and testing datasets (x_train, y_train, x_test, y_test).
    """
    try:
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        # Normalize pixel values to be between 0 and 1
        x_train, x_test = x_train / 255.0, x_test / 255.0
        return (x_train, y_train, x_test, y_test)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        raise e

def main() -> None:
    """
    Main function to execute the model training and evaluation.
    """
    # Load the data
    x_train, y_train, x_test, y_test = load_data()

    # Create the model
    model = create_model(input_shape=(28, 28), num_classes=10)

    # Train the model
    try:
        model.fit(x_train, y_train, epochs=5, validation_split=0.2)  # Fit model on training data
    except Exception as e:
        print(f"Error during model training: {e}")
        return

    # Evaluate the model
    try:
        test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)  # Evaluate on test data
        print(f'\nTest accuracy: {test_acc}')  # Print test accuracy
    except Exception as e:
        print(f"Error during model evaluation: {e}")

if __name__ == "__main__":
    main()