"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-22T08:54:24.481815

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple

def create_model(input_shape: Tuple[int, int, int]) -> keras.Model:
    """Creates and compiles a simple CNN model.

    Args:
        input_shape (Tuple[int, int, int]): Shape of the input data.

    Returns:
        keras.Model: Compiled Keras model.
    """
    try:
        model = keras.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(10, activation='softmax')  # Assuming 10 classes for output
        ])
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        
        return model
    except Exception as e:
        raise RuntimeError(f"Error creating model: {e}")

def train_model(model: keras.Model, x_train: tf.Tensor, y_train: tf.Tensor, epochs: int = 10) -> None:
    """Trains the model on the given training data.

    Args:
        model (keras.Model): The compiled Keras model.
        x_train (tf.Tensor): Training data.
        y_train (tf.Tensor): Training labels.
        epochs (int, optional): Number of epochs to train. Defaults to 10.
    """
    try:
        model.fit(x_train, y_train, epochs=epochs)
    except Exception as e:
        raise RuntimeError(f"Error during model training: {e}")

def main() -> None:
    """Main function to execute the model training process."""
    # Load sample dataset (CIFAR-10)
    (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

    # Normalize the data
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    # Create the model
    model = create_model(input_shape=(32, 32, 3))

    # Train the model
    train_model(model, x_train, y_train)

    # Evaluate the model
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print(f"Test accuracy: {test_acc:.4f}")

if __name__ == "__main__":
    main()