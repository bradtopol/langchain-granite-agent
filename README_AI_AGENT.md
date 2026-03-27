# Simple AI Agent

A lightweight, rule-based conversational AI agent built in Python.

## Features

- **Conversational Interface**: Interactive chat-based interaction
- **Intent Detection**: Recognizes user intents from natural language
- **Multiple Capabilities**:
  - Greetings and farewells
  - Current time queries
  - Current date queries
  - Help and capability information
  - Self-identification
- **Conversation History**: Tracks all interactions with timestamps
- **Extensible Design**: Easy to add new intents and handlers

## Usage

### Running the Agent Interactively

```bash
python ai_agent.py
```

This will start an interactive session where you can chat with the AI agent.

### Using the Agent in Your Code

```python
from ai_agent import SimpleAIAgent

# Create an agent instance
agent = SimpleAIAgent(name="Bob")

# Process user input
response = agent.process_input("Hello!")
print(response)

# Get conversation history
history = agent.get_conversation_history()

# Clear history if needed
agent.clear_history()
```

## Example Conversation

```
You: Hello!
Bob: Hello! I'm Bob, your AI assistant. How can I help you today?

You: What time is it?
Bob: The current time is 02:23 PM.

You: What can you do?
Bob: I can help you with:
- Greet you and have a conversation
- Tell you the current time
- Tell you today's date
- Answer questions about myself
- Provide general assistance

You: Goodbye
Bob: Goodbye! It was nice talking to you. Have a great day!
```

## Architecture

The agent uses a simple rule-based approach:

1. **Intent Detection**: Matches keywords in user input to predefined intents
2. **Handler Functions**: Each intent has a dedicated handler function
3. **Response Generation**: Handlers generate appropriate responses
4. **History Tracking**: All interactions are logged with timestamps

## Extending the Agent

To add new capabilities:

1. Add keywords to `knowledge_base` dictionary
2. Create a handler function (e.g., `_handle_new_intent`)
3. Register the handler in `intent_handlers` dictionary

Example:

```python
# In __init__
self.knowledge_base["weather"] = ["weather", "temperature", "forecast"]
self.intent_handlers["weather"] = self._handle_weather

# Add handler method
def _handle_weather(self, user_input: str) -> str:
    return "I don't have access to weather data yet, but that's a great feature to add!"
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## License

Created with Bob - Feel free to use and modify!