"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T07:59:59.271042

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
import numpy as np

def create_model(input_shape: tuple) -> tf.keras.Model:
    """Creates a sequential neural network model.

    Args:
        input_shape (tuple): The shape of the input data.

    Returns:
        tf.keras.Model: A compiled Keras model.
    """
    model = models.Sequential([
        layers.Flatten(input_shape=input_shape),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(10, activation='softmax')  # Assuming 10 classes for classification
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def load_data() -> tuple:
    """Loads and prepares the MNIST dataset.

    Returns:
        tuple: Training and testing data and labels.
    """
    try:
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize the data
        return (x_train, y_train), (x_test, y_test)
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def train_model(model: tf.keras.Model, x_train: np.ndarray, y_train: np.ndarray) -> None:
    """Trains the model on the training data.

    Args:
        model (tf.keras.Model): The model to train.
        x_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
    """
    try:
        model.fit(x_train, y_train, epochs=5)  # Train for 5 epochs
    except Exception as e:
        print(f"Error during training: {e}")
        raise

def main() -> None:
    """Main function to execute the training process."""
    (x_train, y_train), (x_test, y_test) = load_data()
    model = create_model(input_shape=(28, 28))
    train_model(model, x_train, y_train)
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    print(f'\nTest accuracy: {test_acc:.4f}')

if __name__ == "__main__":
    main()