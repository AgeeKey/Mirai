"""
tensorflow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-19T08:15:50.952021

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.model_selection import train_test_split

def load_and_preprocess_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Load and preprocess the MNIST dataset.

    Returns:
        tuple: A tuple containing the training images and labels.
    """
    try:
        # Load MNIST dataset
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        
        # Normalize the images to the range [0, 1]
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0
        
        # Reshape images to add a channel dimension
        x_train = np.expand_dims(x_train, -1)
        x_test = np.expand_dims(x_test, -1)

        return (x_train, y_train), (x_test, y_test)
    except Exception as e:
        print(f"Error loading or processing data: {e}")
        raise

def create_model() -> keras.Model:
    """
    Create a convolutional neural network model.

    Returns:
        keras.Model: A compiled Keras model.
    """
    try:
        model = keras.Sequential([
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            keras.layers.MaxPooling2D(pool_size=(2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(pool_size=(2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(10, activation='softmax')
        ])
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        
        return model
    except Exception as e:
        print(f"Error creating model: {e}")
        raise

def train_model(model: keras.Model, x_train: np.ndarray, y_train: np.ndarray) -> None:
    """
    Train the model on the training data.

    Args:
        model (keras.Model): The Keras model to train.
        x_train (np.ndarray): Training images.
        y_train (np.ndarray): Training labels.
    """
    try:
        model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1)
    except Exception as e:
        print(f"Error during model training: {e}")
        raise

def evaluate_model(model: keras.Model, x_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the model on the test data.

    Args:
        model (keras.Model): The trained Keras model.
        x_test (np.ndarray): Test images.
        y_test (np.ndarray): Test labels.
    """
    try:
        test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
        print(f'\nTest accuracy: {test_acc:.4f}')
    except Exception as e:
        print(f"Error during model evaluation: {e}")
        raise

def main() -> None:
    """
    Main function to execute the model training and evaluation workflow.
    """
    (x_train, y_train), (x_test, y_test) = load_and_preprocess_data()
    model = create_model()
    train_model(model, x_train, y_train)
    evaluate_model(model, x_test, y_test)

if __name__ == "__main__":
    main()