"""
Simple PennyLane Quantum Circuit Example
A beginner-friendly project demonstrating basic quantum operations with PennyLane.
"""

import pennylane as qml
import numpy as np
import matplotlib.pyplot as plt
import os

# Create a device (quantum simulator)
# 'default.qubit' is a local simulator - no API key needed
dev = qml.device('default.qubit', wires=2)

@qml.qnode(dev)
def quantum_circuit(params):
    """
    A simple variational quantum circuit.
    
    Args:
        params: Rotation angles for the quantum gates
        
    Returns:
        Expectation value of Pauli-Z operator on qubit 0
    """
    # Apply rotation gates
    qml.RY(params[0], wires=0)
    qml.RY(params[1], wires=1)
    
    # Entangle the qubits with a CNOT gate
    qml.CNOT(wires=[0, 1])
    
    # Apply another rotation
    qml.RY(params[2], wires=0)
    
    # Measure the expectation value of Pauli-Z on qubit 0
    return qml.expval(qml.PauliZ(0))

def optimize_circuit():
    """
    Optimize the quantum circuit parameters to minimize the expectation value.
    """
    print("Initializing quantum circuit optimization...")
    
    # Initialize random parameters with gradient tracking enabled
    # Using qml.numpy ensures compatibility with PennyLane's autograd
    params = qml.numpy.array(np.random.random(3), requires_grad=True)
    print(f"Initial parameters: {params}")
    
    # Create an optimizer
    opt = qml.GradientDescentOptimizer(stepsize=0.4)
    
    # Optimize for a few steps
    print("\nOptimizing...")
    for i in range(10):
        params = opt.step(quantum_circuit, params)
        cost = quantum_circuit(params)
        print(f"Step {i+1}: Cost = {cost:.4f}, Params = {params}")
    
    print(f"\nFinal parameters: {params}")
    print(f"Final cost: {quantum_circuit(params):.4f}")
    
    return params

def visualize_circuit():
    """
    Visualize the quantum circuit structure and save to file.
    """
    print("\n" + "="*50)
    print("Quantum Circuit Visualization:")
    print("="*50)
    
    # Text visualization
    circuit_text = qml.draw(quantum_circuit)([0.1, 0.2, 0.3])
    print(circuit_text)
    print("="*50)
    
    # Create visual diagram and save to file
    print("\nGenerating visual circuit diagram...")
    try:
        # Create output directory if it doesn't exist
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate matplotlib figure
        fig, ax = qml.draw_mpl(quantum_circuit)([0.1, 0.2, 0.3])
        
        # Save the figure
        output_path = os.path.join(output_dir, "quantum_circuit.png")
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        print(f"✓ Circuit diagram saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Note: Could not generate visual diagram ({e})")
        print("Text visualization is still available above.")
        return None

if __name__ == "__main__":
    print("="*50)
    print("PennyLane Quantum Circuit Demo")
    print("="*50)
    
    # Visualize the circuit
    output_file = visualize_circuit()
    
    # Run optimization
    print("\n")
    final_params = optimize_circuit()
    
    # Create visualization with final optimized parameters
    if final_params is not None:
        print("\nGenerating optimized circuit visualization...")
        try:
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            fig, ax = qml.draw_mpl(quantum_circuit)(final_params)
            optimized_path = os.path.join(output_dir, "quantum_circuit_optimized.png")
            fig.savefig(optimized_path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            
            print(f"✓ Optimized circuit diagram saved to: {optimized_path}")
        except Exception as e:
            print(f"Note: Could not generate optimized diagram ({e})")
    
    print("\n" + "="*50)
    print("Demo completed successfully!")
    if output_file:
        print(f"Check the 'output' directory for visualization files!")
    print("="*50)

