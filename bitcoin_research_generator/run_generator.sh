#!/bin/bash
# Script to run the Bitcoin Research Index Page Generator

# Change to the base directory where this script is located
cd "$(dirname "$0")/.."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 to run this script."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    . venv/bin/activate
    pip install -r bitcoin_research_generator/requirements.txt
else
    . venv/bin/activate
fi

# Run the generator script
echo "Running Bitcoin Research Index Generator..."
python bitcoin_research_generator/generate_research_page.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "Successfully generated Bitcoin research index page."
    echo "Output file: $(pwd)/blog/bitcoin-research-index.html"
else
    echo "Error generating Bitcoin research index page. Check the logs for details."
fi

# Deactivate virtual environment
deactivate 