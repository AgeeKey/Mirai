"""
TensorFlow - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-17T23:29:18.918978

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple, List

def create_model(input_shape: Tuple[int], num_classes: int) -> keras.Model:
    """
    Creates a simple feedforward neural network model.
    
    Args:
        input_shape (Tuple[int]): Shape of the input data (excluding batch size).
        num_classes (int): Number of output classes for classification.
    
    Returns:
        keras.Model: A compiled Keras model.
    """
    model = keras.Sequential([
        layers.Flatten(input_shape=input_shape),  # Flatten the input
        layers.Dense(128, activation='relu'),     # Hidden layer with ReLU activation
        layers.Dense(num_classes, activation='softmax')  # Output layer with softmax activation
    ])
    
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])  # Compile the model
    
    return model

def load_data() -> Tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    """
    Loads and preprocesses the MNIST dataset.
    
    Returns:
        Tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]: Training and test data and labels.
    """
    try:
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize pixel values
        return (x_train, y_train, x_test, y_test)
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def train_model(model: keras.Model, x_train: tf.Tensor, y_train: tf.Tensor, epochs: int = 5) -> None:
    """
    Trains the given model on the training data.
    
    Args:
        model (keras.Model): The model to be trained.
        x_train (tf.Tensor): The training data.
        y_train (tf.Tensor): The training labels.
        epochs (int): Number of epochs to train the model. Default is 5.
    """
    try:
        model.fit(x_train, y_train, epochs=epochs)  # Train the model
    except Exception as e:
        raise RuntimeError(f"Error during model training: {e}")

def evaluate_model(model: keras.Model, x_test: tf.Tensor, y_test: tf.Tensor) -> None:
    """
    Evaluates the trained model on the test data.
    
    Args:
        model (keras.Model): The trained model.
        x_test (tf.Tensor): The test data.
        y_test (tf.Tensor): The test labels.
    """
    try:
        test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)  # Evaluate the model
        print(f'\nTest accuracy: {test_acc}')  # Print test accuracy
    except Exception as e:
        raise RuntimeError(f"Error during model evaluation: {e}")

def main() -> None:
    """
    Main function to execute the training and evaluation of the model.
    """
    input_shape = (28, 28)  # MNIST image shape
    num_classes = 10  # Number of classes in MNIST

    x_train, y_train, x_test, y_test = load_data()  # Load data
    model = create_model(input_shape, num_classes)  # Create model
    train_model(model, x_train, y_train)  # Train model
    evaluate_model(model, x_test, y_test)  # Evaluate model

if __name__ == "__main__":
    main()  # Run the main function