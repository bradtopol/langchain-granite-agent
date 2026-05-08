#!/bin/bash
# NemoClaw Execution Script
# Runs text analysis examples with the NemoClaw orchestrator

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}NemoClaw Text Analysis${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Error: python3 not found${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${YELLOW}Warning: Ollama server not responding${NC}"
    echo "Please make sure Ollama is running:"
    echo "  1. Install Ollama: https://ollama.ai"
    echo "  2. Start server: ollama serve"
    echo "  3. Pull model: ollama pull granite4:micro"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run based on argument
if [ $# -eq 0 ]; then
    # Default: interactive mode
    echo -e "${GREEN}Starting interactive mode...${NC}"
    echo ""
    python3 example_analysis.py interactive
elif [ "$1" == "example1" ]; then
    echo -e "${GREEN}Running Example 1: AI in Healthcare${NC}"
    echo ""
    python3 example_analysis.py example1
elif [ "$1" == "example2" ]; then
    echo -e "${GREEN}Running Example 2: Climate Change${NC}"
    echo ""
    python3 example_analysis.py example2
elif [ "$1" == "example3" ]; then
    echo -e "${GREEN}Running Example 3: Remote Work${NC}"
    echo ""
    python3 example_analysis.py example3
elif [ "$1" == "interactive" ] || [ "$1" == "-i" ]; then
    echo -e "${GREEN}Starting interactive mode...${NC}"
    echo ""
    python3 example_analysis.py interactive
else
    echo "Unknown option: $1"
    echo ""
    echo "Usage:"
    echo "  ./run_nemoclaw.sh              # Interactive mode (default)"
    echo "  ./run_nemoclaw.sh example1     # AI in Healthcare"
    echo "  ./run_nemoclaw.sh example2     # Climate Change"
    echo "  ./run_nemoclaw.sh example3     # Remote Work"
    echo "  ./run_nemoclaw.sh interactive  # Interactive mode"
    exit 1
fi

# Made with Bob