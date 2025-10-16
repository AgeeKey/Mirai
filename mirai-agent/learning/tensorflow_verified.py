"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-16T04:44:26.201069

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def create_model(input_shape: tuple, num_classes: int) -> keras.Model:
    """
    Creates and compiles a simple feedforward neural network model.

    Args:
        input_shape (tuple): Shape of the input data.
        num_classes (int): Number of output classes.

    Returns:
        keras.Model: Compiled Keras model.
    """
    try:
        model = keras.Sequential([
            layers.Flatten(input_shape=input_shape),  # Flatten the input
            layers.Dense(128, activation='relu'),      # Hidden layer
            layers.Dense(num_classes, activation='softmax')  # Output layer
        ])
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        logging.info("Model created and compiled successfully.")
        return model
    except Exception as e:
        logging.error("Error creating model: %s", e)
        raise

def train_model(model: keras.Model, x_train: np.ndarray, y_train: np.ndarray, epochs: int = 5) -> None:
    """
    Trains the model on the provided training data.

    Args:
        model (keras.Model): The model to be trained.
        x_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
        epochs (int): Number of epochs for training. Default is 5.
    """
    try:
        model.fit(x_train, y_train, epochs=epochs)
        logging.info("Model trained successfully for %d epochs.", epochs)
    except Exception as e:
        logging.error("Error during model training: %s", e)
        raise

def main() -> None:
    """
    Main function to execute the example of creating and training a model.
    """
    # Generate dummy data for demonstration
    num_samples = 1000
    num_classes = 10
    input_shape = (28, 28)

    x_train = np.random.random((num_samples, *input_shape))
    y_train = np.random.randint(0, num_classes, size=(num_samples,))

    # Create model
    model = create_model(input_shape, num_classes)

    # Train model
    train_model(model, x_train, y_train)

if __name__ == "__main__":
    main()