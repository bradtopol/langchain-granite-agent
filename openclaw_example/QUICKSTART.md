# OpenClaw Quick Start Guide

Get up and running with OpenClaw in 5 minutes!

## 📋 Prerequisites Checklist

- [ ] Python 3.8 or higher installed
- [ ] Ollama installed and running
- [ ] Granite 4 Micro model downloaded

## 🚀 Step-by-Step Setup

### Step 1: Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai](https://ollama.ai)

### Step 2: Start Ollama Server

```bash
ollama serve
```

Keep this terminal open. Ollama runs on `http://localhost:11434`

### Step 3: Download Granite 4 Micro

In a new terminal:
```bash
ollama pull granite4:micro
```

This downloads the ~2GB model. Wait for completion.

### Step 4: Verify Setup

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Verify model is installed
ollama list | grep granite4:micro
```

You should see `granite4:micro` in the list.

### Step 5: Install Python Dependencies

```bash
cd openclaw_example
pip install -r requirements.txt
```

## 🎯 Running Your First Research

### Option 1: Use the Run Script (Easiest)

```bash
./run_openclaw.sh
```

This will:
1. Check prerequisites
2. Create virtual environment
3. Install dependencies
4. Start interactive mode

### Option 2: Run Python Directly

```bash
python3 example_research.py interactive
```

### Option 3: Run a Pre-built Example

```bash
# AI in Healthcare example
python3 example_research.py example1

# Quantum Computing example
python3 example_research.py example2

# Climate Change example
python3 example_research.py example3
```

## 💡 Your First Research Task

When the interactive prompt appears:

```
Research Topic: The future of renewable energy
```

Press Enter and watch the magic happen! 🎩✨

You'll see:
1. **Planner Agent** creating a research plan
2. **Researcher Agent** gathering information
3. **Writer Agent** synthesizing the final report

The entire process takes 1.5-2.5 minutes.

## 📊 Understanding the Output

### During Execution

```
======================================================================
🔬 OpenClaw Research Orchestration
======================================================================

Topic: The future of renewable energy
Model: granite4:micro
Agents: 3

======================================================================

======================================================================
Step 1/3: PLANNER
======================================================================

🤖 planner (Strategic Planner)
======================================================================
Goal: Break down research topics into clear, actionable subtasks
Task: The future of renewable energy
----------------------------------------------------------------------

💭 Thinking...

✓ Completed
```

### Final Output

```
======================================================================
FINAL RESEARCH REPORT
======================================================================

EXECUTIVE SUMMARY

The future of renewable energy is characterized by...

[Full comprehensive report]

======================================================================
✓ Research completed in 127.45s
======================================================================
```

## 🎨 Customizing Your Research

### Change the Model

```python
from orchestrator import OpenClawOrchestrator

orchestrator = OpenClawOrchestrator(model="llama2")
result = orchestrator.run_research("Your topic")
```

### Access Individual Agent Outputs

```python
result = orchestrator.run_research("Your topic")

print("PLAN:")
print(result.plan)

print("\nRESEARCH:")
print(result.research)

print("\nFINAL REPORT:")
print(result.report)
```

### Programmatic Usage

```python
from orchestrator import OpenClawOrchestrator

# Initialize
orchestrator = OpenClawOrchestrator()

# Run research
result = orchestrator.run_research(
    topic="Artificial intelligence in education"
)

# Check success
if result.success:
    print(f"✓ Completed in {result.execution_time:.2f}s")
    print(result.final_output)
else:
    print(f"✗ Failed: {result.error}")
```

## 🔧 Common Issues & Solutions

### Issue: "Cannot connect to Ollama server"

**Solution:**
```bash
# Start Ollama in a separate terminal
ollama serve
```

### Issue: "Model not found"

**Solution:**
```bash
# Download the model
ollama pull granite4:micro

# Verify installation
ollama list
```

### Issue: "Import errors"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Agent execution timeout"

**Solution:**
- Check your internet connection
- Verify Ollama is running: `curl http://localhost:11434/api/tags`
- Try a simpler research topic first
- Check system resources (CPU/RAM)

### Issue: "Slow execution"

**Tips to improve speed:**
- Use a smaller model: `model="granite4:micro"` (already the smallest)
- Reduce max_tokens in agent configurations
- Close other applications to free up resources
- Consider using GPU if available

## 📚 Next Steps

### 1. Try Different Topics

```
- "The impact of blockchain on finance"
- "Advances in quantum computing"
- "Climate change mitigation strategies"
- "The future of space exploration"
- "Ethical considerations in AI development"
```

### 2. Explore the Code

- `agents/base_agent.py` - See how agents work
- `orchestrator.py` - Understand orchestration logic
- `models.py` - Learn about data structures

### 3. Customize Agents

Edit agent prompts in:
- `agents/planner_agent.py`
- `agents/researcher_agent.py`
- `agents/writer_agent.py`

### 4. Build Your Own Workflow

```python
from agents import PlannerAgent, ResearcherAgent, WriterAgent
from models import Context, AgentResult

# Create custom workflow
planner = PlannerAgent()
researcher = ResearcherAgent()
writer = WriterAgent()

# Execute manually
context = Context(original_request="Your topic")

plan_result = planner.execute("Your topic", {})
context.add_result("planner", AgentResult(
    agent_name="planner",
    success=plan_result["success"],
    output=plan_result["output"]
))

# Continue with researcher and writer...
```

## 🎓 Learning Resources

### Understanding Multi-Agent Systems

OpenClaw demonstrates key concepts:
- **Agent Specialization**: Each agent has a specific role
- **Sequential Orchestration**: Agents execute in order
- **Context Sharing**: Agents share accumulated knowledge
- **Prompt Engineering**: Specialized prompts for each role

### Architecture Patterns

```
Sequential:  A → B → C → D
Parallel:    A → [B, C, D] → E
Conditional: A → (if X then B else C) → D
Hierarchical: Manager → [Worker1, Worker2, Worker3]
```

OpenClaw uses **Sequential** orchestration.

## 💬 Getting Help

### Check Logs

```bash
# Verbose mode shows detailed execution
python3 example_research.py interactive
```

### Test Individual Components

```python
# Test Ollama connection
from orchestrator import OpenClawOrchestrator
orch = OpenClawOrchestrator()
print(orch.check_ollama_connection())

# Test single agent
from agents import PlannerAgent
planner = PlannerAgent()
result = planner.execute("Test topic", {})
print(result)
```

### Verify Installation

```bash
# Check Python version
python3 --version

# Check installed packages
pip list | grep requests

# Check Ollama
ollama --version
ollama list
```

## 🎉 Success!

You're now ready to use OpenClaw for multi-agent research orchestration!

Try running:
```bash
./run_openclaw.sh
```

And enter your first research topic. Enjoy! 🚀

---

**Need more help?** Check the full [README.md](README.md) for detailed documentation.

**Made with Bob** 🤖