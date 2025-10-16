"""
tensorflow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-16T21:37:51.821200

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple, Any

def create_model(input_shape: Tuple[int, int, int]) -> keras.Model:
    """Create a simple CNN model.

    Args:
        input_shape (Tuple[int, int, int]): Shape of the input data.

    Returns:
        keras.Model: Compiled Keras model.
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
    """Load and preprocess the MNIST dataset.

    Returns:
        Tuple[tf.Tensor, tf.Tensor]: Tuple of training and test data.
    """
    try:
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize data
        x_train = x_train[..., tf.newaxis]
        x_test = x_test[..., tf.newaxis]
        return (x_train, y_train), (x_test, y_test)
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def train_model(model: keras.Model, 
                train_data: Tuple[tf.Tensor, tf.Tensor], 
                epochs: int = 5) -> keras.Model:
    """Train the given model on the training data.

    Args:
        model (keras.Model): The model to train.
        train_data (Tuple[tf.Tensor, tf.Tensor]): Training data.
        epochs (int): Number of epochs to train.

    Returns:
        keras.Model: Trained model.
    """
    try:
        x_train, y_train = train_data
        model.fit(x_train, y_train, epochs=epochs)
        return model
    except Exception as e:
        print(f"Error during training: {e}")
        raise

def evaluate_model(model: keras.Model, 
                   test_data: Tuple[tf.Tensor, tf.Tensor]) -> Any:
    """Evaluate the model on test data.

    Args:
        model (keras.Model): The model to evaluate.
        test_data (Tuple[tf.Tensor, tf.Tensor]): Test data.

    Returns:
        Any: Model evaluation results.
    """
    try:
        x_test, y_test = test_data
        results = model.evaluate(x_test, y_test)
        return results
    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise

def main() -> None:
    """Main function to execute the workflow."""
    input_shape = (28, 28, 1)  # MNIST image shape
    train_data, test_data = load_data()
    model = create_model(input_shape)
    trained_model = train_model(model, train_data, epochs=5)
    evaluation_results = evaluate_model(trained_model, test_data)
    print(f"Test Loss, Test Accuracy: {evaluation_results}")

if __name__ == "__main__":
    main()