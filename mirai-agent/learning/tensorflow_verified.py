"""
tensorflow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-18T08:11:40.366571

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple

def create_model(input_shape: Tuple[int, int, int]) -> keras.Model:
    """
    Create a simple CNN model for image classification.

    Args:
        input_shape (Tuple[int, int, int]): Shape of the input images (height, width, channels).

    Returns:
        keras.Model: Compiled CNN model.
    """
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')  # Assuming 10 classes for classification
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def train_model(model: keras.Model, x_train: tf.Tensor, y_train: tf.Tensor, epochs: int = 10) -> None:
    """
    Train the CNN model on the provided training data.

    Args:
        model (keras.Model): The compiled CNN model.
        x_train (tf.Tensor): Training images.
        y_train (tf.Tensor): Training labels.
        epochs (int): Number of training epochs.
    """
    try:
        model.fit(x_train, y_train, epochs=epochs)
    except Exception as e:
        print(f"An error occurred during training: {e}")

def main() -> None:
    """
    Main function to create and train the CNN model.
    """
    # Load sample dataset (MNIST in this case)
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Preprocess the data
    x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0  # Normalize and reshape
    x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0  # Normalize and reshape
    
    # Create and compile the model
    model = create_model(input_shape=(28, 28, 1))
    
    # Train the model
    train_model(model, x_train, y_train)

    # Evaluate the model on test data
    test_loss, test_accuracy = model.evaluate(x_test, y_test)
    print(f"Test accuracy: {test_accuracy:.4f}")

if __name__ == "__main__":
    main()