#!/bin/bash

echo "⚡ Starting Dashlox Setup..."

# Upgrade pip and install the required packages
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Launching Dashlox App..."

# Run the main server file
python3 src/backend/main.py
