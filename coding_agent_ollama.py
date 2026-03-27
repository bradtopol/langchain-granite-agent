#!/usr/bin/env python3
"""
Custom Coding Agent using Ollama
A simple coding agent that can write, save, and execute code using Ollama's Granite model
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, List

try:
    import requests
except ImportError:
    print("Error: 'requests' module is not installed.")
    print("Please install it using: pip install requests")
    sys.exit(1)


class OllamaCodingAgent:
    """A coding agent that uses Ollama to write and execute code"""
    
    def __init__(self, model: str = "granite3-dense:2b", workspace: str = "workspace"):
        """
        Initialize the coding agent
        
        Args:
            model: The Ollama model to use
            workspace: Directory to save generated files
        """
        self.model = model
        self.base_url = "http://localhost:11434"
        self.chat_url = f"{self.base_url}/api/chat"
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.conversation_history: List[Dict[str, str]] = []
        
        # System prompt for the coding agent
        self.system_prompt = """You are a coding agent. Your job is to:
1. Write clean, well-documented code
2. Save code to files in the workspace directory
3. Test code by running it
4. Provide clear explanations of what you're doing

When writing code:
- Use proper formatting and comments
- Include error handling
- Test the code after writing it

When you need to save a file, use this format:
SAVE_FILE: filename.ext
```language
code content here
```

When you need to run a command, use this format:
RUN_COMMAND: command to execute
"""
    
    def check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def chat(self, message: str, stream: bool = True) -> Optional[str]:
        """
        Send a message to the agent
        
        Args:
            message: User message
            stream: Whether to stream the response
            
        Returns:
            The agent's response
        """
        # Add system prompt if this is the first message
        if not self.conversation_history:
            self.conversation_history.append({
                "role": "system",
                "content": self.system_prompt
            })
        
        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        try:
            payload = {
                "model": self.model,
                "messages": self.conversation_history,
                "stream": stream
            }
            
            response = requests.post(self.chat_url, json=payload, timeout=120)
            
            if response.status_code == 200:
                full_response = ""
                
                if stream:
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line)
                            if 'message' in data and 'content' in data['message']:
                                chunk = data['message']['content']
                                print(chunk, end='', flush=True)
                                full_response += chunk
                    print()
                else:
                    data = response.json()
                    full_response = data.get('message', {}).get('content', '')
                    print(full_response)
                
                # Add assistant response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": full_response
                })
                
                # Process any commands in the response
                self.process_response(full_response)
                
                return full_response
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error in chat: {e}")
            return None
    
    def process_response(self, response: str):
        """
        Process the agent's response for file saves and command execution
        
        Args:
            response: The agent's response text
        """
        lines = response.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for file save command
            if line.startswith('SAVE_FILE:'):
                filename = line.split('SAVE_FILE:')[1].strip()
                i += 1
                
                # Find the code block
                if i < len(lines) and lines[i].strip().startswith('```'):
                    i += 1  # Skip the opening ```
                    code_lines = []
                    
                    while i < len(lines) and not lines[i].strip().startswith('```'):
                        code_lines.append(lines[i])
                        i += 1
                    
                    code = '\n'.join(code_lines)
                    self.save_file(filename, code)
            
            # Check for command execution
            elif line.startswith('RUN_COMMAND:'):
                command = line.split('RUN_COMMAND:')[1].strip()
                self.run_command(command)
            
            i += 1
    
    def save_file(self, filename: str, content: str):
        """
        Save content to a file in the workspace
        
        Args:
            filename: Name of the file
            content: Content to save
        """
        filepath = self.workspace / filename
        
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"\n✓ Saved file: {filepath}")
        except Exception as e:
            print(f"\n✗ Error saving file {filepath}: {e}")
    
    def run_command(self, command: str):
        """
        Execute a shell command in the workspace directory
        
        Args:
            command: Command to execute
        """
        print(f"\n→ Running command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                print(f"Output:\n{result.stdout}")
            if result.stderr:
                print(f"Error:\n{result.stderr}")
            
            if result.returncode == 0:
                print("✓ Command executed successfully")
            else:
                print(f"✗ Command failed with exit code {result.returncode}")
                
        except subprocess.TimeoutExpired:
            print("✗ Command timed out")
        except Exception as e:
            print(f"✗ Error executing command: {e}")
    
    def clear_history(self):
        """Clear conversation history (keeps system prompt)"""
        system_msg = self.conversation_history[0] if self.conversation_history else None
        self.conversation_history = [system_msg] if system_msg else []


def main():
    """Main function"""
    print("=" * 70)
    print("Ollama Coding Agent")
    print("Using model: granite3-dense:2b")
    print("=" * 70)
    print()
    
    # Initialize agent
    agent = OllamaCodingAgent(model="granite3-dense:2b", workspace="workspace")
    
    # Check connection
    print("Checking Ollama connection...")
    if not agent.check_connection():
        print("❌ Error: Cannot connect to Ollama server.")
        print("Please make sure Ollama is running and the model is installed.")
        print("\nTo install the model, run:")
        print("  ollama pull granite3-dense:2b")
        return
    
    print("✓ Connected to Ollama server")
    print(f"✓ Workspace directory: {agent.workspace.absolute()}")
    print()
    
    # Example task
    print("Sending task to agent...")
    print("-" * 70)
    print()
    
    # Configuration for default task
    DEFAULT_TASK = "Write a hello world program in Python and save it to hello.py and test it using python3"
    
    # Allow task customization via command-line arguments or environment variable
    task = os.getenv('CODING_TASK', DEFAULT_TASK)
    if len(sys.argv) > 1:
        task = ' '.join(sys.argv[1:])
    
    # Validate task input
    if not task or not task.strip():
        print("⚠️  Warning: Empty task provided, using default task")
        task = DEFAULT_TASK
    
    print(f"Task: {task}\n")
    print("Agent response:")
    print("-" * 70)
    
    response = agent.chat(task, stream=True)
    
    print()
    print("-" * 70)
    print("\nTask completed!")
    print(f"\nCheck the '{agent.workspace}' directory for generated files.")


if __name__ == "__main__":
    main()

# Made with Bob
