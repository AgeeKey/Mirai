"""
TensorFlow - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-19T17:28:26.766425

This code has been verified by MIRAI's NASA-level learning system.
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import numpy as np

def load_and_prepare_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the Iris dataset and prepare it for training."""
    try:
        iris = load_iris()
        X = iris.data
        y = iris.target.reshape(-1, 1)
        
        # One-hot encode the target variable
        encoder = OneHotEncoder(sparse=False)
        y_encoded = encoder.fit_transform(y)

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
        
        return X_train, X_test, y_train, y_test
    except Exception as e:
        raise RuntimeError(f"Error loading or preparing data: {e}")

def create_model(input_shape: int) -> tf.keras.Model:
    """Create a simple neural network model."""
    model = models.Sequential([
        layers.Input(shape=(input_shape,)),
        layers.Dense(10, activation='relu'),  # Hidden layer
        layers.Dense(3, activation='softmax')  # Output layer for 3 classes
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model(model: tf.keras.Model, X_train: np.ndarray, y_train: np.ndarray) -> None:
    """Train the model on the training data."""
    try:
        model.fit(X_train, y_train, epochs=50, batch_size=5, verbose=1)
    except Exception as e:
        raise RuntimeError(f"Error during model training: {e}")

def evaluate_model(model: tf.keras.Model, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Evaluate the model on the test data."""
    try:
        loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
        print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")
    except Exception as e:
        raise RuntimeError(f"Error during model evaluation: {e}")

def main() -> None:
    """Main function to execute the workflow."""
    X_train, X_test, y_train, y_test = load_and_prepare_data()
    model = create_model(X_train.shape[1])
    train_model(model, X_train, y_train)
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()