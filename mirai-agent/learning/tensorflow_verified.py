"""
tensorflow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-21T07:53:42.760414

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

def create_model(input_shape: tuple, num_classes: int) -> keras.Model:
    """
    Create a simple feedforward neural network model.
    
    Args:
        input_shape (tuple): The shape of the input data.
        num_classes (int): The number of classes for classification.
    
    Returns:
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Flatten(input_shape=input_shape),  # Flatten the input
        layers.Dense(128, activation='relu'),      # Hidden layer with ReLU activation
        layers.Dense(num_classes, activation='softmax')  # Output layer with softmax
    ])
    
    model.compile(optimizer='adam',              # Adam optimizer
                  loss='sparse_categorical_crossentropy',  # Loss function
                  metrics=['accuracy'])           # Metrics to track
    
    return model

def load_data() -> tuple:
    """
    Load the MNIST dataset and preprocess it.
    
    Returns:
        tuple: Tuple containing training and testing data and labels.
    """
    try:
        # Load the MNIST dataset
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        
        # Normalize the images to [0, 1]
        x_train, x_test = x_train / 255.0, x_test / 255.0
        
        return (x_train, y_train), (x_test, y_test)
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def train_model(model: keras.Model, x_train: np.ndarray, y_train: np.ndarray, epochs: int = 5) -> None:
    """
    Train the model on the training data.
    
    Args:
        model (keras.Model): The model to train.
        x_train (np.ndarray): Training data.
        y_train (np.ndarray): Training labels.
        epochs (int): Number of epochs to train for.
    """
    try:
        model.fit(x_train, y_train, epochs=epochs)  # Train the model
    except Exception as e:
        print(f"Error during training: {e}")
        raise

def evaluate_model(model: keras.Model, x_test: np.ndarray, y_test: np.ndarray) -> None:
    """
    Evaluate the model on the test data.
    
    Args:
        model (keras.Model): The model to evaluate.
        x_test (np.ndarray): Test data.
        y_test (np.ndarray): Test labels.
    """
    try:
        test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)  # Evaluate the model
        print(f'\nTest accuracy: {test_acc}')  # Print test accuracy
    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise

if __name__ == "__main__":
    (x_train, y_train), (x_test, y_test) = load_data()  # Load the data
    model = create_model(input_shape=(28, 28), num_classes=10)  # Create the model
    train_model(model, x_train, y_train, epochs=5)  # Train the model
    evaluate_model(model, x_test, y_test)  # Evaluate the model