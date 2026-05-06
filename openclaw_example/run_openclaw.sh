#!/bin/bash
# Run OpenClaw Orchestration Example

echo "=================================="
echo "OpenClaw Orchestration Runner"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Error: Ollama server is not running"
    echo ""
    echo "Please start Ollama:"
    echo "  ollama serve"
    echo ""
    exit 1
fi

echo "✓ Python 3 found"
echo "✓ Ollama server is running"
echo ""

# Check if granite4:micro is installed
if ! ollama list | grep -q "granite4:micro"; then
    echo "⚠️  Warning: granite4:micro model not found"
    echo ""
    echo "Installing granite4:micro..."
    ollama pull granite4:micro
    echo ""
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run the example
echo "=================================="
echo "Starting OpenClaw..."
echo "=================================="
echo ""

# Check for command line argument
if [ $# -eq 0 ]; then
    # No arguments - run interactive mode
    python3 example_research.py interactive
else
    # Pass arguments to the script
    python3 example_research.py "$@"
fi

# Made with Bob