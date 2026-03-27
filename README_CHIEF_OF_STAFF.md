# Chief of Staff Agent 🎯

An intelligent Chief of Staff assistant powered by Ollama's Granite model. This agent helps you manage tasks, coordinate activities, make decisions, and provide strategic support.

## Features

### 🎯 Core Capabilities

1. **Task Management**
   - Create and track tasks with priorities
   - Update task status (pending, in progress, completed)
   - View task summaries and lists
   - Automatic task context in conversations

2. **Strategic Planning**
   - Decision tracking and recommendations
   - Multi-option analysis
   - Context-aware suggestions
   - Strategic thinking support

3. **Note Taking**
   - Quick note capture
   - Categorized notes
   - Timestamped entries
   - Easy retrieval

4. **Communication Support**
   - Natural language interaction
   - Context-aware responses
   - Professional communication style
   - Summary generation

5. **State Persistence**
   - Save and load agent state
   - Preserve tasks, notes, and decisions
   - Resume sessions seamlessly

## Prerequisites

1. **Ollama** - Install from [ollama.ai](https://ollama.ai)
2. **Python 3.7+**
3. **Required Python packages**: `requests`

## Installation

1. Install Ollama and start the server:
```bash
ollama serve
```

2. Pull the Granite model:
```bash
ollama pull granite3-dense:2b
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the agent using the provided script:
```bash
./run_chief_of_staff.sh
```

Or run directly with Python:
```bash
python3 chief_of_staff_agent.py
```

### Commands

#### Task Management
```
add task <title>          - Add a new task
list tasks                - Show all tasks
complete <id>             - Mark task as completed
status                    - Show current status summary
```

#### Notes & Decisions
```
add note <content>        - Add a note
list notes                - Show all notes
add decision <title>      - Record a decision point
```

#### General Commands
```
summary                   - Generate comprehensive status summary
save                      - Save current state to file
load                      - Load saved state from file
clear                     - Clear conversation history
help                      - Show help message
quit/exit                 - End session
```

### Natural Language Interaction

You can also interact naturally with the agent:

```
You: Help me prioritize my tasks for today

You: What should I consider when deciding between option A and B?

You: Create a summary of what we've accomplished this week

You: Break down this complex project into manageable steps

You: What are the key risks I should be aware of?
```

## Example Session

```
You: add task Review quarterly reports
✓ Task added: #1 - Review quarterly reports

You: add task Prepare presentation for board meeting
✓ Task added: #2 - Prepare presentation for board meeting

You: list tasks
📋 TASKS:
  ○ #1 [medium] Review quarterly reports (pending)
  ○ #2 [medium] Prepare presentation for board meeting (pending)

You: Help me prioritize these tasks
Agent: Based on your current tasks, I recommend prioritizing the board 
meeting presentation first, as it likely has a fixed deadline and high 
visibility. The quarterly reports can be reviewed after, as they provide 
important context for the presentation...

You: complete 1
✓ Task #1 marked as completed!

You: summary
📊 CURRENT STATUS SUMMARY
==================================================
Tasks: 1 pending, 0 in progress, 1 completed
Notes: 0 recorded
Decisions: 0 tracked

📋 RECENT TASKS:
  ✓ [medium] Review quarterly reports
  ○ [medium] Prepare presentation for board meeting
```

## Features in Detail

### Task Management
- **Priority Levels**: low, medium, high
- **Status Tracking**: pending, in_progress, completed, cancelled
- **Timestamps**: Creation and completion times
- **Context Integration**: Tasks automatically included in relevant conversations

### Decision Support
- **Structured Decision Records**: Title, context, options, recommendations
- **Historical Tracking**: Review past decisions
- **Analysis Support**: AI-powered decision analysis
- **Recommendation Engine**: Get strategic recommendations

### State Persistence
The agent automatically saves state to `chief_of_staff_state.json`:
- All tasks with their status
- Notes and categories
- Decision records
- Timestamps for everything

Load previous state on startup or manually with the `load` command.

## Architecture

### Components

1. **ChiefOfStaffAgent Class**
   - Main agent logic
   - Ollama integration
   - State management
   - Context enhancement

2. **Task Management System**
   - CRUD operations for tasks
   - Status tracking
   - Priority management

3. **Note System**
   - Quick capture
   - Categorization
   - Retrieval

4. **Decision Tracking**
   - Structured decision records
   - Option analysis
   - Recommendation tracking

### AI Integration

The agent uses Ollama's Granite model with:
- **Streaming responses** for real-time interaction
- **Context enhancement** with relevant data
- **Conversation history** for continuity
- **System prompts** for role definition

## Customization

### Change the Model

Edit `chief_of_staff_agent.py`:
```python
agent = ChiefOfStaffAgent(model="your-model-name")
```

### Modify System Prompt

The system prompt defines the agent's behavior. Edit the `system_prompt` in the `__init__` method to customize:
- Communication style
- Capabilities
- Focus areas
- Response format

### Add Custom Commands

Add new command handlers in the `main()` function:
```python
if user_input.lower().startswith("your command"):
    # Your command logic here
    continue
```

## Tips for Best Results

1. **Be Specific**: Provide clear context when asking for help
2. **Use Commands**: Leverage built-in commands for structured data
3. **Save Regularly**: Use `save` command to preserve your work
4. **Review Summaries**: Use `summary` to get overview of current state
5. **Natural Interaction**: Don't hesitate to chat naturally about your work

## Troubleshooting

### Connection Issues
```
❌ Error: Cannot connect to Ollama server
```
**Solution**: Make sure Ollama is running with `ollama serve`

### Model Not Found
```
❌ Error: Model not found
```
**Solution**: Pull the model with `ollama pull granite3-dense:2b`

### Slow Responses
- Try a smaller model
- Check system resources
- Ensure Ollama has adequate memory

### State Not Loading
- Check if `chief_of_staff_state.json` exists
- Verify JSON format is valid
- Check file permissions

## Advanced Usage

### Programmatic Integration

Use the agent in your own Python code:

```python
from chief_of_staff_agent import ChiefOfStaffAgent

# Initialize
agent = ChiefOfStaffAgent()

# Add tasks
task = agent.add_task("Important task", priority="high")

# Chat
response = agent.chat("Help me plan my day", stream=False)

# Get summary
summary = agent.generate_summary()

# Save state
agent.save_state("my_state.json")
```

### Batch Operations

Create multiple tasks from a list:
```python
tasks = [
    "Review code changes",
    "Update documentation",
    "Schedule team meeting"
]

for task_title in tasks:
    agent.add_task(task_title)
```

## Future Enhancements

Potential additions:
- Calendar integration
- Email drafting
- Meeting notes
- Project templates
- Team collaboration features
- Analytics and insights
- Reminder system
- File attachments

## Contributing

Feel free to extend this agent with additional features:
1. Add new command handlers
2. Enhance the system prompt
3. Integrate with external services
4. Add new data structures
5. Improve the UI/UX

## License

This project is created with Bob and is available for personal and commercial use.

## Credits

- Built with [Ollama](https://ollama.ai)
- Powered by Granite models
- Made with Bob

---

**Need help?** Type `help` in the agent or refer to this README.

**Ready to boost your productivity?** Run `./run_chief_of_staff.sh` and start organizing!