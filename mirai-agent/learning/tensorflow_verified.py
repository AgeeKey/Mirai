"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-18T15:49:32.607622

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
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])
    
    return model

def load_data() -> Tuple[tf.Tensor, tf.Tensor]:
    """Loads and preprocesses the MNIST dataset.

    Returns:
        Tuple[tf.Tensor, tf.Tensor]: Tuple of training and testing data (images, labels).
    """
    try:
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        # Normalize the images to the range [0, 1]
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0
        
        # Reshape data to include channel dimension
        x_train = x_train.reshape((-1, 28, 28, 1))
        x_test = x_test.reshape((-1, 28, 28, 1))
        
        return (x_train, y_train), (x_test, y_test)
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def train_model(model: keras.Model, data: Tuple[tf.Tensor, tf.Tensor], epochs: int = 5) -> None:
    """Trains the model on the provided data.

    Args:
        model (keras.Model): The Keras model to train.
        data (Tuple[tf.Tensor, tf.Tensor]): Training data (images, labels).
        epochs (int): Number of epochs to train for.
    """
    (x_train, y_train), (x_test, y_test) = data
    try:
        model.fit(x_train, y_train, epochs=epochs, validation_data=(x_test, y_test))
    except Exception as e:
        print(f"Error during training: {e}")
        raise

def main() -> None:
    """Main function to run the training process."""
    input_shape = (28, 28, 1)  # MNIST images shape
    model = create_model(input_shape)
    data = load_data()
    train_model(model, data)

if __name__ == "__main__":
    main()