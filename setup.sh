#!/bin/bash

# Detect OS
os=$(uname)

# Install Redis based on OS
if [ "$os" == "Linux" ]; then
    echo "Installing Redis on Linux..."
    sudo apt update
    sudo apt install redis-server
    sudo systemctl enable redis
    sudo systemctl start redis
elif [ "$os" == "Darwin" ]; then
    echo "Installing Redis on macOS..."
    brew install redis
    brew services start redis
else
    echo "Unsupported OS. Please install Redis manually."
    exit 1
fi

# Install Python requirements
echo "Installing Python requirements..."
pip install -r requirements.txt

source .env
echo "Setup complete"