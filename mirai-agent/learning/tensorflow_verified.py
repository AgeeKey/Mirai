"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-21T22:29:17.724720

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
        input_shape (tuple): Shape of the input data.
        num_classes (int): Number of output classes.

    Returns:
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Flatten(input_shape=input_shape),  # Flatten the input
        layers.Dense(128, activation='relu'),      # Hidden layer with ReLU activation
        layers.Dropout(0.2),                        # Dropout layer for regularization
        layers.Dense(num_classes, activation='softmax')  # Output layer with softmax activation
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def load_data() -> tuple:
    """
    Loads the MNIST dataset and preprocesses it.

    Returns:
        tuple: Tuple of training and test data (x_train, y_train, x_test, y_test).
    """
    try:
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        # Normalize the images to [0, 1] range
        x_train, x_test = x_train / 255.0, x_test / 255.0
        return x_train, y_train, x_test, y_test
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def train_model(model: keras.Model, x_train: np.ndarray, y_train: np.ndarray, epochs: int = 5) -> None:
    """
    Trains the model on the training data.

    Args:
        model (keras.Model): The model to train.
        x_train (np.ndarray): Training features.
        y_train (np.ndarray): Training labels.
        epochs (int): Number of epochs to train.
    """
    try:
        model.fit(x_train, y_train, epochs=epochs)
    except Exception as e:
        print(f"Error during model training: {e}")
        raise

def evaluate_model(model: keras.Model, x_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluates the model on the test data.

    Args:
        model (keras.Model): The model to evaluate.
        x_test (np.ndarray): Test features.
        y_test (np.ndarray): Test labels.
    """
    try:
        test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
        print(f'Test accuracy: {test_acc:.4f}')
    except Exception as e:
        print(f"Error during model evaluation: {e}")
        raise

def main() -> None:
    """
    Main function to run the training and evaluation of the model.
    """
    input_shape = (28, 28)  # MNIST images are 28x28
    num_classes = 10  # Digits 0-9

    x_train, y_train, x_test, y_test = load_data()  # Load and preprocess data
    model = create_model(input_shape, num_classes)   # Create the model
    train_model(model, x_train, y_train, epochs=5)    # Train the model
    evaluate_model(model, x_test, y_test)              # Evaluate the model

if __name__ == "__main__":
    main()  # Run the main function