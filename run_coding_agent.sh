#!/bin/bash
# Launch script for Ollama Coding Agent
# This script opens a new Terminal window and runs the coding agent

cd "$(dirname "$0")"

osascript <<EOF
tell application "Terminal"
    activate
    do script "cd '$PWD' && python3 coding_agent_ollama.py"
end tell
EOF

# Made with Bob
