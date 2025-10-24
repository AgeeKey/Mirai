import numpy as np

class LionOptimizer:
    def __init__(self, learning_rate=0.001, beta=0.9):
        self.learning_rate = learning_rate
        self.beta = beta
        self.momentum = None

    def update(self, params, grads):
        if self.momentum is None:
            self.momentum = np.zeros_like(grads)
        
        # Update momentum
        self.momentum = self.beta * self.momentum + (1 - self.beta) * np.sign(grads)
        
        # Update parameters
        params -= self.learning_rate * self.momentum
        
        return params

# Example usage
if __name__ == "__main__":
    # Initial parameters and gradients
    params = np.array([1.0, 2.0, 3.0])
    grads = np.array([0.1, -0.2, 0.3])
    
    # Initialize optimizer
    optimizer = LionOptimizer(learning_rate=0.01, beta=0.9)
    
    # Update parameters
    updated_params = optimizer.update(params, grads)
    
    print("Updated parameters:", updated_params)