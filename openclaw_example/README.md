# OpenClaw - Multi-Agent Orchestration Framework

A simple yet powerful multi-agent orchestration framework that demonstrates how specialized AI agents collaborate to complete complex research tasks.

## 🎯 Overview

OpenClaw orchestrates three specialized agents in a sequential workflow to conduct comprehensive research:

```
User Request → Planner → Researcher → Writer → Final Report
```

### Agents

1. **Planner Agent** 🗺️
   - **Role**: Strategic Planner
   - **Goal**: Break down research topics into actionable subtasks
   - **Output**: Structured research plan with 3-5 subtasks

2. **Researcher Agent** 🔍
   - **Role**: Research Specialist
   - **Goal**: Conduct thorough research on each subtask
   - **Output**: Detailed findings with examples and implications

3. **Writer Agent** ✍️
   - **Role**: Research Writer
   - **Goal**: Synthesize research into comprehensive report
   - **Output**: Professional research report with executive summary

## 🏗️ Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Orchestrator                     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Planner    │→ │  Researcher  │→ │    Writer    │     │
│  │    Agent     │  │    Agent     │  │    Agent     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         ↓                 ↓                  ↓              │
│  ┌──────────────────────────────────────────────────┐     │
│  │              Shared Context                       │     │
│  │  • Original Request                               │     │
│  │  • Agent Results                                  │     │
│  │  • Accumulated Knowledge                          │     │
│  └──────────────────────────────────────────────────┘     │
│                          ↓                                  │
│                   Granite 4 Micro                          │
│                   (via Ollama)                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. User provides research topic
   ↓
2. Orchestrator initializes Context
   ↓
3. Planner Agent:
   - Receives: Topic
   - Creates: Research plan with subtasks
   - Adds to Context
   ↓
4. Researcher Agent:
   - Receives: Topic + Plan from Context
   - Conducts: Research on each subtask
   - Adds to Context
   ↓
5. Writer Agent:
   - Receives: Topic + Plan + Research from Context
   - Creates: Final comprehensive report
   - Adds to Context
   ↓
6. Orchestrator returns OrchestrationResult
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
   ```bash
   python3 --version
   ```

2. **Ollama** (with Granite 4 Micro)
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama server
   ollama serve
   
   # Pull Granite 4 Micro model
   ollama pull granite4:micro
   ```

### Installation

```bash
# Clone or navigate to the openclaw_example directory
cd openclaw_example

# Install dependencies
pip install -r requirements.txt
```

### Running Examples

#### Option 1: Interactive Mode (Default)
```bash
./run_openclaw.sh
# or
python3 example_research.py interactive
```

#### Option 2: Pre-built Examples
```bash
# Example 1: AI in Healthcare
./run_openclaw.sh example1

# Example 2: Quantum Computing
./run_openclaw.sh example2

# Example 3: Climate Change Solutions
./run_openclaw.sh example3
```

## 📖 Usage

### Basic Usage

```python
from orchestrator import OpenClawOrchestrator

# Initialize orchestrator
orchestrator = OpenClawOrchestrator(model="granite4:micro")

# Run research
result = orchestrator.run_research(
    topic="The impact of artificial intelligence on healthcare"
)

# Access results
if result.success:
    print(result.final_output)  # Complete report
    print(result.plan)          # Planner's output
    print(result.research)      # Researcher's output
    print(result.report)        # Writer's output (same as final_output)
```

### Advanced Usage

```python
from orchestrator import OpenClawOrchestrator
from models import Context, OrchestrationResult

# Custom configuration
orchestrator = OpenClawOrchestrator(
    model="granite4:micro",
    base_url="http://localhost:11434",
    verbose=True
)

# Check Ollama connection
if not orchestrator.check_ollama_connection():
    print("Ollama is not running!")
    exit(1)

# Show agent information
orchestrator.print_agent_info()

# Run research
result = orchestrator.run_research("Your research topic")

# Access individual agent results
for agent_name, agent_result in result.context.results.items():
    print(f"\n{agent_name.upper()}:")
    print(agent_result.output)
    print(f"Timestamp: {agent_result.timestamp}")
```

## 🔧 Configuration

### Agent Configuration

Each agent can be customized with different parameters:

```python
from agents import PlannerAgent, ResearcherAgent, WriterAgent

# Custom Planner
planner = PlannerAgent(
    model="granite4:micro",
    base_url="http://localhost:11434",
    temperature=0.5  # Lower for more structured output
)

# Custom Researcher
researcher = ResearcherAgent(
    model="granite4:micro",
    temperature=0.6  # Balanced for factual research
)

# Custom Writer
writer = WriterAgent(
    model="granite4:micro",
    temperature=0.7  # Higher for more creative writing
)
```

### Model Configuration

OpenClaw supports any Ollama-compatible model:

```python
# Use different models
orchestrator = OpenClawOrchestrator(model="llama2")
orchestrator = OpenClawOrchestrator(model="mistral")
orchestrator = OpenClawOrchestrator(model="granite3-dense:2b")
```

## 📁 Project Structure

```
openclaw_example/
├── agents/
│   ├── __init__.py           # Agent package exports
│   ├── base_agent.py         # Base agent class with LLM integration
│   ├── planner_agent.py      # Planning agent
│   ├── researcher_agent.py   # Research agent
│   └── writer_agent.py       # Writing agent
├── models.py                 # Data models (Task, Context, Result)
├── orchestrator.py           # Main orchestration engine
├── example_research.py       # Example usage and interactive mode
├── requirements.txt          # Python dependencies
├── run_openclaw.sh          # Execution script
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── QUICKSTART.md            # Quick start guide
```

## 🎓 Key Concepts

### 1. Agent Specialization
Each agent has a specific role, goal, and expertise:
- **Planner**: Strategic thinking and task decomposition
- **Researcher**: Information gathering and analysis
- **Writer**: Content synthesis and report creation

### 2. Sequential Orchestration
Agents execute in a defined order, with each agent building on previous work:
```
Plan → Research → Write
```

### 3. Context Sharing
All agents share a common context that accumulates knowledge:
```python
context = {
    "original_request": "Research topic",
    "planner": "Research plan",
    "researcher": "Research findings",
    "writer": "Final report"
}
```

### 4. Prompt Engineering
Each agent uses specialized prompts optimized for their role:
- Planner: Structured planning format
- Researcher: Comprehensive research template
- Writer: Professional report structure

## 🔍 Example Output

### Input
```
Topic: "The impact of artificial intelligence on healthcare"
```

### Planner Output
```
RESEARCH PLAN: AI in Healthcare

SUBTASK 1: Diagnostic Applications
- Research Question: How is AI improving medical diagnosis?
- Key Areas: Image analysis, pattern recognition, early detection
- Expected Outcome: Understanding of AI diagnostic tools

SUBTASK 2: Treatment Optimization
...
```

### Researcher Output
```
RESEARCH FINDINGS

SUBTASK 1: Diagnostic Applications
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Key Findings:
• AI achieves 95%+ accuracy in medical imaging
• Early detection rates improved by 30%
...
```

### Writer Output
```
EXECUTIVE SUMMARY

Artificial intelligence is revolutionizing healthcare through...

INTRODUCTION

The healthcare industry is experiencing a transformative shift...

MAIN FINDINGS

1. Diagnostic Applications
   AI-powered diagnostic tools have demonstrated remarkable...
...
```

## 🛠️ Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Verify model is installed
ollama list | grep granite4:micro
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python3 --version  # Should be 3.8+
```

### Agent Execution Failures
- Check Ollama logs for errors
- Verify model is loaded: `ollama list`
- Increase timeout in base_agent.py if needed
- Check temperature settings (0.0-1.0 range)

## 🚧 Extending OpenClaw

### Adding New Agents

1. Create a new agent class:
```python
from agents.base_agent import BaseAgent

class AnalystAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="analyst",
            role="Data Analyst",
            goal="Analyze research data",
            backstory="Expert data analyst...",
            **kwargs
        )
    
    def create_prompt(self, task, context):
        # Custom prompt logic
        return f"Analyze: {task}"
```

2. Add to orchestrator workflow:
```python
self.analyst = AnalystAgent(model=model)
self.agents = [self.planner, self.researcher, self.analyst, self.writer]
```

### Custom Workflows

Create parallel or conditional workflows:
```python
# Parallel execution
results = []
for agent in [agent1, agent2, agent3]:
    result = agent.execute(task, context)
    results.append(result)

# Conditional execution
if planner_result.contains("technical"):
    researcher = TechnicalResearcher()
else:
    researcher = GeneralResearcher()
```

## 📊 Performance

Typical execution times (with Granite 4 Micro):
- **Planner**: 10-20 seconds
- **Researcher**: 30-60 seconds
- **Writer**: 40-80 seconds
- **Total**: 80-160 seconds (1.5-2.5 minutes)

Performance depends on:
- Model size and speed
- Hardware (CPU/GPU)
- Prompt complexity
- Token limits

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Parallel agent execution
- Agent communication protocols
- Tool integration (web search, file operations)
- Streaming output support
- Error recovery mechanisms
- Performance optimizations

## 📝 License

This project is created for educational purposes to demonstrate multi-agent orchestration patterns.

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.ai) for local LLM inference
- Powered by IBM's [Granite 4 Micro](https://www.ibm.com/granite) model
- Inspired by frameworks like CrewAI and LangGraph

---

**Made with Bob** 🤖

For questions or issues, please refer to the QUICKSTART.md guide or check the troubleshooting section above.