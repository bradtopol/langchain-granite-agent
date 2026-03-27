#!/usr/bin/env python3
"""
Simple Ollama Application with Granite Model
A conversational AI application using Ollama's Granite model
"""

import json
import sys
from typing import Optional, List, Dict
from datetime import datetime

# Check for required dependencies
try:
    import requests
except ImportError:
    print("Error: 'requests' module is not installed.")
    print("\nPlease install it using:")
    print("  pip install requests")
    print("or")
    print("  pip install -r requirements.txt")
    sys.exit(1)


class OllamaGraniteApp:
    """Simple application to interact with Ollama's Granite model"""
    
    def __init__(self, model: str = "granite3-dense:2b", base_url: str = "http://localhost:11434"):
        """
        Initialize the Ollama Granite application
        
        Args:
            model: The Granite model to use (default: granite3-dense:2b - a small 2B parameter model)
            base_url: The Ollama API base URL
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.chat_url = f"{base_url}/api/chat"
        self.conversation_history: List[Dict[str, str]] = []
    
    def check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def list_models(self) -> Optional[List[str]]:
        """List available models in Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error listing models: {e}")
            return None
    
    def generate(self, prompt: str, stream: bool = False) -> Optional[str]:
        """
        Generate a response from the Granite model
        
        Args:
            prompt: The input prompt
            stream: Whether to stream the response
            
        Returns:
            The generated response or None if error
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream
            }
            
            response = requests.post(self.api_url, json=payload, timeout=60)
            
            if response.status_code == 200:
                if stream:
                    # Handle streaming response
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line)
                            if 'response' in data:
                                chunk = data['response']
                                print(chunk, end='', flush=True)
                                full_response += chunk
                    print()  # New line after streaming
                    return full_response
                else:
                    # Handle non-streaming response
                    data = response.json()
                    return data.get('response', '')
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error generating response: {e}")
            return None
    
    def chat(self, message: str, stream: bool = False) -> Optional[str]:
        """
        Chat with the Granite model (maintains conversation context)
        
        Args:
            message: The user message
            stream: Whether to stream the response
            
        Returns:
            The assistant's response or None if error
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
            
            payload = {
                "model": self.model,
                "messages": self.conversation_history,
                "stream": stream
            }
            
            response = requests.post(self.chat_url, json=payload, timeout=60)
            
            if response.status_code == 200:
                if stream:
                    # Handle streaming response
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line)
                            if 'message' in data and 'content' in data['message']:
                                chunk = data['message']['content']
                                print(chunk, end='', flush=True)
                                full_response += chunk
                    print()  # New line after streaming
                    
                    # Add assistant response to history
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": full_response
                    })
                    return full_response
                else:
                    # Handle non-streaming response
                    data = response.json()
                    assistant_message = data.get('message', {}).get('content', '')
                    
                    # Add assistant response to history
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    return assistant_message
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error in chat: {e}")
            return None
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history"""
        return self.conversation_history


def main():
    """Main function to run the Ollama Granite application"""
    print("=" * 70)
    print("Ollama Granite Application")
    print("Using model: granite3-dense:2b (small 2B parameter model)")
    print("=" * 70)
    print()
    
    # Initialize the app
    app = OllamaGraniteApp(model="granite3-dense:2b")
    
    # Check connection
    print("Checking Ollama connection...")
    if not app.check_connection():
        print("❌ Error: Cannot connect to Ollama server.")
        print("Please make sure Ollama is running (ollama serve)")
        print("And that you have the granite3-dense:2b model installed.")
        print("\nTo install the model, run:")
        print("  ollama pull granite3-dense:2b")
        return
    
    print("✓ Connected to Ollama server")
    print()
    
    # List available models
    print("Available models:")
    models = app.list_models()
    if models:
        for model in models:
            marker = "→" if model == app.model else " "
            print(f"  {marker} {model}")
    print()
    
    print("Commands:")
    print("  - Type your message to chat with Granite")
    print("  - Type 'clear' to clear conversation history")
    print("  - Type 'history' to view conversation history")
    print("  - Type 'quit' or 'exit' to end the session")
    print("=" * 70)
    print()
    
    # Interactive chat loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit"]:
                print("\nGoodbye! Thanks for using Ollama Granite App!")
                break
            
            if user_input.lower() == "clear":
                app.clear_history()
                print("✓ Conversation history cleared.\n")
                continue
            
            if user_input.lower() == "history":
                history = app.get_history()
                if not history:
                    print("No conversation history yet.\n")
                else:
                    print("\n--- Conversation History ---")
                    for msg in history:
                        role = msg['role'].capitalize()
                        content = msg['content']
                        print(f"{role}: {content}")
                    print("--- End of History ---\n")
                continue
            
            # Send message to Granite model
            print("Granite: ", end='', flush=True)
            response = app.chat(user_input, stream=True)
            print()  # Extra newline for readability
            
            if response is None:
                print("Failed to get response from the model.\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Thanks for using Ollama Granite App!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()

# Made with Bob