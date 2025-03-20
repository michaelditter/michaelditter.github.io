#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def create_learning_rate_chart():
    # Set up figure
    plt.figure(figsize=(10, 6))
    
    # Create epochs array
    epochs = np.arange(0, 100)
    
    # Create different learning rate schedules
    
    # Step decay
    def step_decay(epoch, initial_lr=0.1, drop=0.5, epochs_drop=20):
        return initial_lr * np.power(drop, np.floor((1+epoch)/epochs_drop))
    
    # Cosine annealing
    def cosine_annealing(epoch, initial_lr=0.1, min_lr=0.001, max_epochs=100):
        return min_lr + 0.5 * (initial_lr - min_lr) * (1 + np.cos(epoch / max_epochs * np.pi))
    
    # Cyclic learning rate
    def cyclic_lr(epoch, base_lr=0.001, max_lr=0.1, step_size=10):
        cycle = np.floor(1 + epoch / (2 * step_size))
        x = np.abs(epoch / step_size - 2 * cycle + 1)
        return base_lr + (max_lr - base_lr) * np.maximum(0, (1 - x))
    
    # Warm restarts
    def warm_restarts(epoch, initial_lr=0.1, min_lr=0.001, T_0=20, T_mult=2):
        # Calculate the restart cycle
        if epoch == 0:
            return initial_lr
        
        cycle_len = T_0
        cycle_start = 0
        while cycle_start + cycle_len <= epoch:
            cycle_start += cycle_len
            cycle_len *= T_mult
        
        current_epoch = epoch - cycle_start
        return min_lr + 0.5 * (initial_lr - min_lr) * (1 + np.cos(current_epoch / cycle_len * np.pi))
    
    # Apply learning rate schedules to epochs
    step_decay_lr = [step_decay(e) for e in epochs]
    cosine_annealing_lr = [cosine_annealing(e) for e in epochs]
    cyclic_lr_values = [cyclic_lr(e) for e in epochs]
    warm_restarts_lr = [warm_restarts(e) for e in epochs]
    
    # Plotting
    plt.plot(epochs, step_decay_lr, 'b-', label='Step Decay')
    plt.plot(epochs, cosine_annealing_lr, 'r-', label='Cosine Annealing')
    plt.plot(epochs, cyclic_lr_values, 'g-', label='Cyclic LR')
    plt.plot(epochs, warm_restarts_lr, 'm-', label='Warm Restarts')
    
    # Add labels and legend
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Learning Rate', fontsize=12)
    plt.title('Learning Rate Scheduling Methods', fontsize=14, fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Tight layout and save
    plt.tight_layout()
    
    # Create directories if needed
    img_dir = Path("img/blog")
    img_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the chart
    output_path = img_dir / "learning-rate-schedules.jpg"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Created learning rate schedules chart: {output_path}")
    
    # Close the plot
    plt.close()

if __name__ == "__main__":
    create_learning_rate_chart() 