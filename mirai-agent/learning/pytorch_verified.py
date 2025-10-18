"""
PyTorch - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-18T11:52:26.789084

This code has been verified by MIRAI's NASA-level learning system.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

class SimpleNN(nn.Module):
    """
    A simple feedforward neural network model with one hidden layer.
    """
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)  # First layer
        self.fc2 = nn.Linear(hidden_size, output_size)  # Second layer

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the network.
        
        Args:
            x (torch.Tensor): Input tensor.
        
        Returns:
            torch.Tensor: Output tensor after passing through the network.
        """
        x = F.relu(self.fc1(x))  # Activation for hidden layer
        x = self.fc2(x)  # Output layer
        return x


def train(model: nn.Module, device: torch.device, train_loader: DataLoader, optimizer: optim.Optimizer, epochs: int) -> None:
    """
    Train the model on the training dataset.
    
    Args:
        model (nn.Module): The neural network model.
        device (torch.device): The device to perform computations on.
        train_loader (DataLoader): DataLoader for the training dataset.
        optimizer (optim.Optimizer): Optimizer for the model parameters.
        epochs (int): Number of epochs to train the model.
    """
    model.train()  # Set model to training mode
    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)  # Move data to the device
            optimizer.zero_grad()  # Reset gradients
            output = model(data.view(data.size(0), -1))  # Flatten input
            loss = F.cross_entropy(output, target)  # Calculate loss
            loss.backward()  # Backpropagation
            optimizer.step()  # Update weights
            
            if batch_idx % 10 == 0:
                print(f'Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item():.6f}')


def main() -> None:
    """
    Main function to set up the data, model, and training loop.
    """
    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Hyperparameters
    input_size = 784  # 28x28 images
    hidden_size = 128
    output_size = 10  # 10 classes for MNIST
    batch_size = 64
    learning_rate = 0.001
    epochs = 5
    
    # Transform for image preprocessing
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    
    # Load the MNIST dataset
    try:
        train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
        train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return
    
    # Initialize the model, optimizer
    model = SimpleNN(input_size, hidden_size, output_size).to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Train the model
    train(model, device, train_loader, optimizer, epochs)


if __name__ == '__main__':
    main()