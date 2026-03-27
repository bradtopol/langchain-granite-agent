# Ollama Granite Application

A simple Python application for interacting with Ollama's Granite language model. This application uses the small **granite3-dense:2b** model (2 billion parameters) for efficient local AI conversations.

## Features

- **Interactive Chat Interface**: Conversational AI powered by Granite
- **Streaming Responses**: Real-time response generation
- **Conversation History**: Maintains context across messages
- **Connection Checking**: Verifies Ollama server availability
- **Model Listing**: Shows all available Ollama models
- **Simple Commands**: Easy-to-use command interface

## Prerequisites

1. **Install Ollama**: Download and install from [ollama.ai](https://ollama.ai)
2. **Pull the Granite Model**: Run the following command:
   ```bash
   ollama pull granite3-dense:2b
   ```
3. **Start Ollama Server**: 
   ```bash
   ollama serve
   ```

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python ollama_granite_app.py
```

### Interactive Commands

Once the application is running, you can use these commands:

- **Chat**: Simply type your message and press Enter
- **`clear`**: Clear the conversation history
- **`history`**: View the entire conversation history
- **`quit`** or **`exit`**: Exit the application

### Example Session

```
======================================================================
Ollama Granite Application
Using model: granite3-dense:2b (small 2B parameter model)
======================================================================

Checking Ollama connection...
✓ Connected to Ollama server

Available models:
  → granite3-dense:2b
    llama2:latest

Commands:
  - Type your message to chat with Granite
  - Type 'clear' to clear conversation history
  - Type 'history' to view conversation history
  - Type 'quit' or 'exit' to end the session
======================================================================

You: Hello! What can you help me with?
Granite: Hello! I'm an AI assistant powered by the Granite model. I can help you with:
- Answering questions on various topics
- Writing and editing text
- Coding assistance
- Problem-solving
- General conversation
What would you like help with today?

You: Write a Python function to calculate fibonacci numbers
Granite: Here's a Python function to calculate Fibonacci numbers:

def fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Example usage
print(fibonacci(10))  # Output: 55

You: quit
Goodbye! Thanks for using Ollama Granite App!
```

## Using as a Library

You can also import and use the `OllamaGraniteApp` class in your own Python code:

```python
from ollama_granite_app import OllamaGraniteApp

# Initialize the app
app = OllamaGraniteApp(model="granite3-dense:2b")

# Check connection
if app.check_connection():
    # Generate a simple response
    response = app.generate("What is Python?")
    print(response)
    
    # Or use chat mode with context
    response = app.chat("Hello!")
    print(response)
    
    response = app.chat("Tell me a joke")
    print(response)
    
    # Clear history when needed
    app.clear_history()
```

## API Methods

### `OllamaGraniteApp` Class

- **`__init__(model, base_url)`**: Initialize the application
  - `model`: Model name (default: "granite3-dense:2b")
  - `base_url`: Ollama API URL (default: "http://localhost:11434")

- **`check_connection()`**: Check if Ollama server is running
  - Returns: `bool`

- **`list_models()`**: List all available models
  - Returns: `List[str]` or `None`

- **`generate(prompt, stream)`**: Generate a one-off response
  - `prompt`: Input text
  - `stream`: Enable streaming (default: False)
  - Returns: `str` or `None`

- **`chat(message, stream)`**: Chat with context preservation
  - `message`: User message
  - `stream`: Enable streaming (default: False)
  - Returns: `str` or `None`

- **`clear_history()`**: Clear conversation history

- **`get_history()`**: Get conversation history
  - Returns: `List[Dict[str, str]]`

## About Granite Models

Granite is IBM's family of open-source language models. The **granite3-dense:2b** model used in this application is:

- **Small and Efficient**: Only 2 billion parameters
- **Fast**: Quick response times on consumer hardware
- **Capable**: Good performance for general tasks
- **Open Source**: Free to use and modify

### Other Granite Models

You can use other Granite models by changing the model parameter:

- `granite3-dense:2b` - Small, fast (2B parameters)
- `granite3-dense:8b` - Balanced (8B parameters)
- `granite3-moe:3b` - Mixture of Experts (3B parameters)

To use a different model:
```python
app = OllamaGraniteApp(model="granite3-dense:8b")
```

## Troubleshooting

### "Cannot connect to Ollama server"

1. Make sure Ollama is installed
2. Start the Ollama server: `ollama serve`
3. Check if the server is running on port 11434

### "Model not found"

Pull the model first:
```bash
ollama pull granite3-dense:2b
```

### Slow responses

- The 2B model is optimized for speed
- For better quality, try larger models like `granite3-dense:8b`
- Ensure your system has adequate resources

## Requirements

- Python 3.7+
- Ollama installed and running
- `requests` library (see requirements.txt)

## License

Created with Bob - Feel free to use and modify!

## Resources

- [Ollama Official Site](https://ollama.ai)
- [Granite Models on Hugging Face](https://huggingface.co/ibm-granite)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)