#!/bin/bash

# Ensure the results directory exists
mkdir -p results

# Run the simulation and recovery process
echo "Running EZ diffusion model simulation and recovery..."
python3 src/simulate_recover.py > results/output.txt

echo "Simulation complete. Results saved in results/output.txt"
