#!/bin/bash
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y libraqm-dev

echo "Installing Python dependencies..."
pip install -r requirements.txt