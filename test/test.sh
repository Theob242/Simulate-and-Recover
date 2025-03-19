#!/bin/bash

# Ensure tests start fresh
echo "Running tests..."

# Run the main script and capture output
src/main.sh

# Check if output file was created
if [ -s results/output.txt ]; then
    echo "Test Passed: results/output.txt was created and is not empty."
else
    echo "Test Failed: results/output.txt is missing or empty."
    exit 1
fi

# Check for key expected words in the output file
if grep -q "Recovered Parameters" results/output.txt; then
    echo "Test Passed: Simulation produced recovered parameters."
else
    echo "Test Failed: No recovered parameters found in output."
    exit 1
fi

echo "All tests completed successfully."
