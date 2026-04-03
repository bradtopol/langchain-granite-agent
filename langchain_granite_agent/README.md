# LangChain ReAct Agent with Granite 4 Micro

A comprehensive demonstration of the **ReAct (Reasoning and Acting)** pattern using IBM's Granite 4 micro model via Ollama and LangChain. This project showcases how AI agents can reason about tasks, use tools, and complete complex multi-step workflows.

## 🌟 Features

### ReAct Pattern Implementation
- **Thought**: Agent reasons about what needs to be done
- **Action**: Agent selects and uses appropriate tools
- **Observation**: Agent learns from tool outputs
- **Iteration**: Continues until task is complete
- **Final Answer**: Provides comprehensive result

### Three Powerful Tools

#### 🧮 Calculator Tool
- Basic arithmetic operations (+, -, *, /, %, **)
- Advanced functions (sqrt, sin, cos, tan, log, exp)
- Mathematical constants (pi, e)
- Safe expression evaluation

#### 📁 File Operations Tool
- Read file contents
- Write/create files
- List directory contents
- Delete files
- All operations sandboxed to workspace directory

#### 🔍 Web Search Tool
- DuckDuckGo integration (no API key required)
- Returns top search results with snippets
- Useful for current information and research

## 📋 Prerequisites

1. **Python 3.8+**
2. **Ollama** - Install from [ollama.ai](https://ollama.ai)
3. **Granite 4 Micro Model**:
   ```bash
   ollama pull granite4:micro
   ```
4. **Start Ollama Server**:
   ```bash
   ollama serve
   ```

## 🚀 Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd langchain_granite_agent
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Ollama is running**:
   ```bash
   ollama list
   ```
   You should see `granite4:micro` in the list.

## 💻 Usage

### Interactive Mode

Run the agent in interactive mode:

```bash
python langchain_react_agent.py
```

Or use the shell script:

```bash
chmod +x run_agent.sh
./run_agent.sh
```

### Example Queries

Try these queries in interactive mode:

**Simple Calculation:**
```
Calculate 15% of 240
```

**Multi-Step Reasoning:**
```
Calculate 15% of 240, multiply by 3, and save the result to a file called calculation.txt
```

**Web Search:**
```
Search for information about LangChain and summarize the top result
```

**File Operations:**
```
Create a file called languages.txt with a list of 5 programming languages
```

**Complex Workflow:**
```
Search for the latest Python version, calculate 25% of 100, and create a file with both results
```

### Running Examples

Run pre-built example workflows:

```bash
python examples.py
```

This will demonstrate:
- Simple calculations
- Multi-step reasoning
- File creation and reading
- Web searches
- Complex multi-tool workflows

## 📁 Project Structure

```
langchain_granite_agent/
├── README.md                      # This file
├── PLAN.md                        # Detailed implementation plan
├── requirements.txt               # Python dependencies
├── run_agent.sh                   # Shell script to run agent
├── langchain_react_agent.py       # Main ReAct agent implementation
├── examples.py                    # Example workflows
├── tools/                         # Custom tool implementations
│   ├── __init__.py
│   ├── calculator.py              # Mathematical operations
│   ├── file_operations.py         # File read/write/list
│   └── web_search.py              # DuckDuckGo search
└── workspace/                     # Safe directory for file operations
```

## 🔧 Configuration

### Agent Parameters

You can customize the agent in `langchain_react_agent.py`:

```python
agent = GraniteReActAgent(
    model="granite4:micro",        # Ollama model name
    temperature=0.1,               # Lower = more consistent
    workspace_dir="workspace",     # File operations directory
    max_iterations=10,             # Max reasoning steps
    verbose=True                   # Show intermediate steps
)
```

### Tool Configuration

Each tool can be configured independently:

```python
# Calculator - no configuration needed
calculator = CalculatorTool()

# File Operations - custom workspace
file_ops = FileOperationsTool(workspace_dir="custom_workspace")

# Web Search - custom result count
web_search = WebSearchTool(max_results=3)
```

## 🎯 How It Works

### The ReAct Loop

1. **User Query**: "Calculate 15% of 240 and save to a file"

2. **Agent Reasoning**:
   ```
   Thought: I need to calculate 15% of 240 first
   Action: calculator
   Action Input: 0.15 * 240
   Observation: 36
   
   Thought: Now I need to save this to a file
   Action: file_operations
   Action Input: write: result.txt | The result is 36
   Observation: Successfully wrote to result.txt
   
   Thought: I now know the final answer
   Final Answer: I calculated 15% of 240 which is 36, and saved it to result.txt
   ```

### Tool Selection

The agent automatically selects the appropriate tool based on:
- Tool descriptions
- Current task requirements
- Previous observations
- Reasoning about next steps

## 📚 Example Workflows

### Example 1: Simple Math
```python
Query: "What is the square root of 144?"
Result: The agent uses the calculator tool and returns 12
```

### Example 2: Multi-Step Calculation
```python
Query: "Calculate 15% of 240, multiply by 3"
Result: Agent performs two calculations: 36, then 108
```

### Example 3: Research and Document
```python
Query: "Search for LangChain info and create a summary file"
Result: Agent searches web, then creates file with summary
```

### Example 4: File Management
```python
Query: "List all files in workspace and count them"
Result: Agent lists files and provides count
```

## 🛠️ Troubleshooting

### "Cannot connect to Ollama"
- Ensure Ollama is running: `ollama serve`
- Check if running on port 11434
- Verify with: `curl http://localhost:11434/api/tags`

### "Model not found"
- Pull the model: `ollama pull granite4:micro`
- List models: `ollama list`
- Try alternative: `ollama pull granite3-dense:2b`

### "Import errors"
- Install dependencies: `pip install -r requirements.txt`
- Use virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

### "DuckDuckGo search not working"
- Check internet connection
- Verify package: `pip install duckduckgo-search`
- Try updating: `pip install --upgrade duckduckgo-search`

### Agent gets stuck in loop
- Reduce max_iterations
- Simplify the query
- Check tool descriptions are clear
- Increase temperature slightly (0.2-0.3)

## 🔒 Security

### File Operations Safety
- All file operations are restricted to the `workspace` directory
- Path traversal attacks are prevented
- No access to system files outside workspace

### Calculator Safety
- Expression evaluation uses restricted namespace
- Dangerous operations (import, exec, eval) are blocked
- Only safe math functions are available

### Web Search
- Read-only operation
- No data sent to external services except search queries
- Uses DuckDuckGo's privacy-focused API

## 🎓 Learning Resources

### ReAct Pattern
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [LangChain ReAct Documentation](https://python.langchain.com/docs/modules/agents/agent_types/react)

### Granite Models
- [IBM Granite Models](https://www.ibm.com/granite)
- [Granite on Hugging Face](https://huggingface.co/ibm-granite)

### LangChain
- [LangChain Documentation](https://python.langchain.com/)
- [LangChain Agents Guide](https://python.langchain.com/docs/modules/agents/)

### Ollama
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Models](https://ollama.ai/library)

## 🤝 Contributing

This is a demonstration project. Feel free to:
- Add new tools
- Improve prompts
- Enhance error handling
- Add more examples
- Create tests

## 📝 License

Created with Bob - Free to use and modify!

## 🙏 Acknowledgments

- **IBM** for the Granite models
- **LangChain** for the agent framework
- **Ollama** for local model serving
- **DuckDuckGo** for privacy-focused search

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the PLAN.md for implementation details
3. Ensure all prerequisites are met
4. Verify Ollama and model are working independently

## 🚀 Next Steps

After getting familiar with this project:
1. Try creating custom tools
2. Experiment with different models
3. Build multi-agent systems
4. Add memory/conversation history
5. Create a web UI
6. Integrate with databases or APIs

---

**Made with Bob** 🤖

Enjoy exploring AI agents with Granite 4 micro!