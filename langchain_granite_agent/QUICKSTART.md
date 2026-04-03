# Quick Start Guide - LangChain ReAct Agent with Granite 4 Micro

## ⚡ 5-Minute Setup

### 1. Prerequisites Check

```bash
# Check Python version (need 3.8+)
python3 --version

# Check if Ollama is installed
ollama --version
```

### 2. Install Ollama Model

```bash
# Pull Granite 4 micro model
ollama pull granite4-micro

# Start Ollama server (in a separate terminal)
ollama serve
```

### 3. Install Dependencies

```bash
cd langchain_granite_agent
pip3 install -r requirements.txt
```

### 4. Run the Agent

**Option A: Using the shell script**
```bash
./run_agent.sh
```

**Option B: Direct Python**
```bash
python3 langchain_react_agent.py
```

**Option C: Run examples**
```bash
python3 examples.py
```

## 🎯 Try These Queries

Once the agent is running, try these example queries:

### Simple Math
```
Calculate 15% of 240
```

### Multi-Step Reasoning
```
Calculate the square root of 144, add 10, then multiply by 2
```

### File Operations
```
Create a file called notes.txt with a list of 5 programming languages
```

### Web Search
```
Search for information about LangChain and give me a summary
```

### Complex Workflow
```
Calculate 25% of 100, search for the latest Python version, and save both results to a file called results.txt
```

## 🔧 Troubleshooting

### "Cannot connect to Ollama"
```bash
# Start Ollama server
ollama serve
```

### "Model not found"
```bash
# Pull the model
ollama pull granite4-micro
```

### "Import errors"
```bash
# Reinstall dependencies
pip3 install -r requirements.txt
```

## 📚 What's Included

- **3 Custom Tools**: Calculator, File Operations, Web Search
- **ReAct Pattern**: Reasoning and Acting loop
- **8 Example Workflows**: From simple to complex
- **Full Documentation**: README.md and PLAN.md
- **Test Suite**: test_tools.py

## 🎓 Learn More

- Read [README.md](README.md) for complete documentation
- Check [PLAN.md](PLAN.md) for implementation details
- Run `python3 test_tools.py` to test individual tools
- Run `python3 examples.py` to see all example workflows

## 🚀 Next Steps

1. Try the example queries above
2. Create your own custom tools
3. Experiment with different models
4. Build multi-agent systems
5. Add memory and conversation history

---

**Made with Bob** 🤖

Enjoy exploring AI agents!