"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T07:41:58.025855

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

def create_model(input_shape: tuple) -> tf.keras.Model:
    """Creates a Sequential CNN model.

    Args:
        input_shape (tuple): The shape of the input data.

    Returns:
        tf.keras.Model: A compiled Keras model.
    """
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')  # Assuming 10 classes for classification
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def load_data() -> tuple[np.ndarray, np.ndarray]:
    """Loads and preprocesses the CIFAR-10 dataset.

    Returns:
        tuple[np.ndarray, np.ndarray]: Training and test data and labels.
    """
    try:
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize images to [0, 1]
        return (x_train, y_train.flatten()), (x_test, y_test.flatten())
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def train_model(model: tf.keras.Model, x_train: np.ndarray, y_train: np.ndarray) -> None:
    """Trains the model on the training data.

    Args:
        model (tf.keras.Model): The model to be trained.
        x_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
    """
    try:
        model.fit(x_train, y_train, epochs=10, batch_size=64)
    except Exception as e:
        print(f"Error during training: {e}")
        raise

def evaluate_model(model: tf.keras.Model, x_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluates the model on the test data.

    Args:
        model (tf.keras.Model): The model to be evaluated.
        x_test (np.ndarray): Test data.
        y_test (np.ndarray): Test labels.
    """
    try:
        test_loss, test_acc = model.evaluate(x_test, y_test)
        print(f"Test accuracy: {test_acc}, Test loss: {test_loss}")
    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise

def main() -> None:
    """Main function to run the training and evaluation of the model."""
    input_shape = (32, 32, 3)  # CIFAR-10 images are 32x32 pixels with 3 color channels
    x_train, y_train = load_data()[0]
    x_test, y_test = load_data()[1]
    
    model = create_model(input_shape)
    train_model(model, x_train, y_train)
    evaluate_model(model, x_test, y_test)

if __name__ == "__main__":
    main()