"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-21T04:58:44.464499

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
import numpy as np

def create_model(input_shape: tuple) -> keras.Model:
    """Creates and compiles a simple neural network model.

    Args:
        input_shape (tuple): Shape of the input data.

    Returns:
        keras.Model: Compiled Keras model.
    """
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=input_shape),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def load_and_preprocess_data() -> tuple:
    """Loads and preprocesses the MNIST dataset.

    Returns:
        tuple: Tuple of training and testing data (X_train, X_test, y_train, y_test).
    """
    try:
        (X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
        X_train, X_test = X_train / 255.0, X_test / 255.0  # Normalize the data
        return X_train, X_test, y_train, y_test
    except Exception as e:
        print(f"Error loading dataset: {e}")
        raise

def main() -> None:
    """Main function to execute the model training and evaluation."""
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    model = create_model(input_shape=(28, 28))  # MNIST images are 28x28 pixels

    try:
        model.fit(X_train, y_train, epochs=5, validation_data=(X_val, y_val))
        test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
        print(f'\nTest accuracy: {test_acc}')
    except Exception as e:
        print(f"Error during training or evaluation: {e}")
        raise

if __name__ == "__main__":
    main()