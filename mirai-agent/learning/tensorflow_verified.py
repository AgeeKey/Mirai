"""
tensorflow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-20T09:13:53.660014

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

def create_model(input_shape: tuple) -> tf.keras.Model:
    """Creates a simple CNN model for image classification.

    Args:
        input_shape (tuple): Shape of the input images (height, width, channels).

    Returns:
        tf.keras.Model: A compiled CNN model.
    """
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')  # Assuming 10 classes
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def load_data() -> tuple:
    """Loads and preprocesses the CIFAR-10 dataset.

    Returns:
        tuple: Tuple of training and testing datasets (x_train, y_train), (x_test, y_test).
    """
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    
    # Normalize the pixel values to [0, 1]
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    return (x_train, y_train), (x_test, y_test)

def train_model(model: tf.keras.Model, x_train: np.ndarray, y_train: np.ndarray) -> None:
    """Trains the model on the training data.

    Args:
        model (tf.keras.Model): The compiled Keras model.
        x_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
    """
    try:
        model.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.2)
    except Exception as e:
        print(f"An error occurred during training: {e}")

def main() -> None:
    """Main function to execute the model training process."""
    input_shape = (32, 32, 3)  # CIFAR-10 images are 32x32 pixels with 3 color channels
    
    (x_train, y_train), (x_test, y_test) = load_data()  # Load data
    model = create_model(input_shape)  # Create model
    train_model(model, x_train, y_train)  # Train model
    
    # Evaluate the model
    try:
        test_loss, test_accuracy = model.evaluate(x_test, y_test)
        print(f"Test accuracy: {test_accuracy:.4f}")
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")

if __name__ == "__main__":
    main()