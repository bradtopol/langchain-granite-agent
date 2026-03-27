#!/bin/bash

# Run the Chief of Staff Agent
# This script starts the Chief of Staff agent with Ollama

echo "Starting Chief of Staff Agent..."
echo "================================"
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Error: Ollama server is not running."
    echo ""
    echo "Please start Ollama first:"
    echo "  ollama serve"
    echo ""
    echo "Then make sure you have the granite3-dense:2b model:"
    echo "  ollama pull granite3-dense:2b"
    echo ""
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed."
    exit 1
fi

# Check if requests module is installed
if ! python3 -c "import requests" 2>/dev/null; then
    echo "⚠️  Warning: 'requests' module not found."
    echo "Installing requirements..."
    pip3 install -r requirements.txt
    echo ""
fi

# Run the agent
python3 chief_of_staff_agent.py

# Made with Bob