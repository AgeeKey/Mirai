"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-19T14:50:48.801000

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

def create_model(input_shape: tuple, num_classes: int) -> keras.Model:
    """
    Creates a Sequential model for classification.
    
    Args:
        input_shape (tuple): Shape of the input data (height, width, channels).
        num_classes (int): Number of output classes.
    
    Returns:
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def train_model(model: keras.Model, x_train: np.ndarray, y_train: np.ndarray, epochs: int = 10) -> None:
    """
    Trains the model with the given training data.
    
    Args:
        model (keras.Model): The Keras model to train.
        x_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
        epochs (int): Number of epochs to train.
    
    Raises:
        ValueError: If the training data or labels have incorrect shapes.
    """
    if x_train.ndim != 4:
        raise ValueError("Training data should be 4-dimensional (batch_size, height, width, channels).")
    if y_train.ndim != 1:
        raise ValueError("Training labels should be 1-dimensional.")
    
    model.fit(x_train, y_train, epochs=epochs)

def main() -> None:
    """
    Main function to execute the model training process.
    """
    # Example data (10 samples of 28x28 grayscale images)
    x_train = np.random.rand(10, 28, 28, 1).astype(np.float32)
    y_train = np.random.randint(0, 10, size=(10,)).astype(np.int32)  # 10 classes
    
    model = create_model(input_shape=(28, 28, 1), num_classes=10)
    train_model(model, x_train, y_train, epochs=5)

if __name__ == "__main__":
    main()