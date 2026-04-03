#!/bin/bash
# Shell script to run the LangChain ReAct Agent with Granite 4 Micro

echo "========================================================================"
echo "  LangChain ReAct Agent with Granite 4 Micro"
echo "========================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if Ollama is running
echo "Checking Ollama connection..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Error: Cannot connect to Ollama server"
    echo ""
    echo "Please make sure:"
    echo "  1. Ollama is installed (https://ollama.ai)"
    echo "  2. Ollama server is running: ollama serve"
    echo "  3. Granite 4 micro model is installed: ollama pull granite4:micro"
    exit 1
fi

echo "✓ Ollama server is running"

# Check if granite4:micro model is available
if ! curl -s http://localhost:11434/api/tags | grep -q "granite4:micro"; then
    echo "⚠️  Warning: granite4:micro model not found"
    echo ""
    echo "To install the model, run:"
    echo "  ollama pull granite4:micro"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ granite4:micro model is available"
fi

# Check if dependencies are installed
echo "Checking Python dependencies..."
if ! python3 -c "import langchain" 2>/dev/null; then
    echo "⚠️  Warning: LangChain not installed"
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install dependencies"
        exit 1
    fi
else
    echo "✓ Dependencies are installed"
fi

echo ""
echo "========================================================================"
echo "  Starting Agent..."
echo "========================================================================"
echo ""

# Run the agent
python3 langchain_react_agent.py

# Made with Bob