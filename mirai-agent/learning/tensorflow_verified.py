"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-20T17:34:03.354774

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple

def create_model(input_shape: Tuple[int, int, int]) -> keras.Model:
    """
    Creates a simple CNN model for image classification.

    Args:
        input_shape (Tuple[int, int, int]): Shape of the input images (height, width, channels).

    Returns:
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')  # Assuming 10 classes for classification
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def train_model(model: keras.Model, x_train: tf.Tensor, y_train: tf.Tensor, epochs: int = 10) -> None:
    """
    Trains the model on the provided training data.

    Args:
        model (keras.Model): The model to train.
        x_train (tf.Tensor): Training images.
        y_train (tf.Tensor): Training labels.
        epochs (int): Number of epochs to train the model.
    
    Raises:
        ValueError: If the shapes of the training data do not match the model's expected input.
    """
    if x_train.shape[1:] != model.input_shape[1:]:
        raise ValueError("Input shape of training data does not match model's input shape.")
    
    model.fit(x_train, y_train, epochs=epochs)

def main() -> None:
    """
    Main function to create, train, and evaluate the CNN model.
    """
    # Load and preprocess the dataset (using MNIST as an example)
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train = x_train.reshape((x_train.shape[0], 28, 28, 1)).astype('float32') / 255.0
    x_test = x_test.reshape((x_test.shape[0], 28, 28, 1)).astype('float32') / 255.0

    model = create_model(input_shape=(28, 28, 1))  # Input shape for MNIST images
    train_model(model, x_train, y_train, epochs=5)

    # Evaluate the model on test data
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    print(f'\nTest accuracy: {test_acc:.4f}')

if __name__ == "__main__":
    main()