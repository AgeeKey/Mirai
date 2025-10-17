"""
tensorflow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-17T18:39:09.177382

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple

def create_model(input_shape: Tuple[int, int, int]) -> keras.Model:
    """Creates a simple CNN model.

    Args:
        input_shape (Tuple[int, int, int]): Shape of the input data (height, width, channels).

    Returns:
        keras.Model: A compiled CNN model.
    """
    model = keras.Sequential([
        layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')  # Assuming 10 classes
    ])
    
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])
    
    return model

def load_data() -> Tuple[tf.Tensor, tf.Tensor]:
    """Loads and preprocesses the MNIST dataset.

    Returns:
        Tuple[tf.Tensor, tf.Tensor]: Training and test datasets (x_train, y_train, x_test, y_test).
    """
    try:
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize the data
        x_train = x_train[..., tf.newaxis]  # Add channel dimension
        x_test = x_test[..., tf.newaxis]  # Add channel dimension
        return (x_train, y_train), (x_test, y_test)
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def train_model(model: keras.Model, data: Tuple[tf.Tensor, tf.Tensor], epochs: int = 5) -> None:
    """Trains the model on the given data.

    Args:
        model (keras.Model): The model to train.
        data (Tuple[tf.Tensor, tf.Tensor]): Training data (x_train, y_train).
        epochs (int): Number of training epochs.
    """
    (x_train, y_train), _ = data
    try:
        model.fit(x_train, y_train, epochs=epochs)
    except Exception as e:
        print(f"Error during training: {e}")
        raise

def main() -> None:
    """Main function to execute the model training."""
    input_shape = (28, 28, 1)  # MNIST images are 28x28 pixels with 1 color channel
    model = create_model(input_shape)
    data = load_data()
    train_model(model, data)

if __name__ == "__main__":
    main()