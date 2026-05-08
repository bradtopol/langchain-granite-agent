# NemoClaw - Simple 2-Agent Orchestration Framework

A lightweight multi-agent orchestration framework that demonstrates how two specialized AI agents collaborate to analyze text content through summarization and deep analysis.

## 🎯 Overview

NemoClaw orchestrates two specialized agents in a sequential workflow to provide comprehensive text analysis:

```
User Text → Summarizer → Analyzer → Complete Analysis
```

### Agents

1. **Summarizer Agent** 📝
   - **Role**: Text Summarizer
   - **Goal**: Extract key points and create concise summaries
   - **Output**: Key points, main themes, and brief summary

2. **Analyzer Agent** 🔍
   - **Role**: Content Analyst
   - **Goal**: Provide insights, patterns, and actionable recommendations
   - **Output**: Insights, patterns, implications, and recommendations

## 🏗️ Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                  NemoClaw Orchestrator                       │
│                                                              │
│  ┌──────────────┐           ┌──────────────┐               │
│  │  Summarizer  │    →      │   Analyzer   │               │
│  │    Agent     │           │    Agent     │               │
│  └──────────────┘           └──────────────┘               │
│         ↓                          ↓                         │
│  ┌──────────────────────────────────────────────────┐      │
│  │              Shared Context                       │      │
│  │  • Original Text                                  │      │
│  │  • Summary (from Summarizer)                      │      │
│  │  • Analysis (from Analyzer)                       │      │
│  └──────────────────────────────────────────────────┘      │
│                          ↓                                   │
│                   Granite 4 Micro                           │
│                   (via Ollama)                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. User provides text content
   ↓
2. Orchestrator initializes Context
   ↓
3. Summarizer Agent:
   - Receives: Original text
   - Extracts: Key points and themes
   - Creates: Concise summary
   - Adds to Context
   ↓
4. Analyzer Agent:
   - Receives: Original text + Summary from Context
   - Identifies: Patterns and insights
   - Provides: Implications and recommendations
   - Adds to Context
   ↓
5. Orchestrator returns OrchestrationResult
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
# Navigate to the nemoclaw_example directory
cd nemoclaw_example

# Install dependencies
pip install -r requirements.txt
```

### Running Examples

#### Option 1: Interactive Mode (Default)
```bash
./run_nemoclaw.sh
# or
python3 example_analysis.py interactive
```

#### Option 2: Pre-built Examples
```bash
# Example 1: AI in Healthcare
./run_nemoclaw.sh example1

# Example 2: Climate Change
./run_nemoclaw.sh example2

# Example 3: Remote Work
./run_nemoclaw.sh example3
```

## 📖 Usage

### Basic Usage

```python
from orchestrator import NemoClawOrchestrator

# Initialize orchestrator
orchestrator = NemoClawOrchestrator(model="granite4:micro")

# Analyze text
text = """
Your text content here...
"""

result = orchestrator.analyze_text(text)

# Access results
if result.success:
    print(result.summary)    # Summarizer's output
    print(result.analysis)   # Analyzer's output
    print(result.final_output)  # Complete analysis
```

### Advanced Usage

```python
from orchestrator import NemoClawOrchestrator
from models import Context, OrchestrationResult

# Custom configuration
orchestrator = NemoClawOrchestrator(
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

# Analyze text
result = orchestrator.analyze_text("Your text here...")

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
from agents import SummarizerAgent, AnalyzerAgent

# Custom Summarizer
summarizer = SummarizerAgent(
    model="granite4:micro",
    base_url="http://localhost:11434",
    temperature=0.5  # Lower for more structured output
)

# Custom Analyzer
analyzer = AnalyzerAgent(
    model="granite4:micro",
    temperature=0.7  # Higher for more creative analysis
)
```

### Model Configuration

NemoClaw supports any Ollama-compatible model:

```python
# Use different models
orchestrator = NemoClawOrchestrator(model="llama2")
orchestrator = NemoClawOrchestrator(model="mistral")
orchestrator = NemoClawOrchestrator(model="granite3-dense:2b")
```

## 📁 Project Structure

```
nemoclaw_example/
├── agents/
│   ├── __init__.py           # Agent package exports
│   ├── base_agent.py         # Base agent class with LLM integration
│   ├── summarizer_agent.py   # Summarization agent
│   └── analyzer_agent.py     # Analysis agent
├── models.py                 # Data models (Task, Context, Result)
├── orchestrator.py           # Main orchestration engine
├── example_analysis.py       # Example usage and interactive mode
├── requirements.txt          # Python dependencies
├── run_nemoclaw.sh          # Execution script
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── QUICKSTART.md            # Quick start guide
```

## 🎓 Key Concepts

### 1. Agent Specialization
Each agent has a specific role and expertise:
- **Summarizer**: Distills information into key points and concise summaries
- **Analyzer**: Provides deep insights, patterns, and actionable recommendations

### 2. Sequential Orchestration
Agents execute in a defined order, with each agent building on previous work:
```
Summarize → Analyze
```

### 3. Context Sharing
Both agents share a common context that accumulates knowledge:
```python
context = {
    "original_request": "Text to analyze",
    "summarizer": "Summary with key points",
    "analyzer": "Deep analysis with insights"
}
```

### 4. Prompt Engineering
Each agent uses specialized prompts optimized for their role:
- Summarizer: Structured extraction of key points and themes
- Analyzer: Deep analysis with insights and recommendations

## 🔍 Example Output

### Input
```
Text about AI in healthcare (300+ words)...
```

### Summarizer Output
```
KEY POINTS:
• AI improving medical diagnostics with 95%+ accuracy
• Treatment personalization through data analysis
• Predictive analytics for early intervention
• Privacy and ethical considerations remain important

MAIN THEMES:
• Healthcare transformation through AI
• Balance between innovation and ethics

SUMMARY:
AI is revolutionizing healthcare through diagnostic tools, 
personalized treatment, and predictive analytics, while raising 
important questions about privacy and the role of human judgment...
```

### Analyzer Output
```
KEY INSIGHTS:
• Healthcare AI adoption accelerating rapidly
• Human-AI collaboration is key to success
• Ethical frameworks need to evolve with technology

PATTERNS & TRENDS:
• Shift from reactive to predictive healthcare
• Increasing focus on personalized medicine

IMPLICATIONS:
• Healthcare costs may decrease long-term
• Medical professionals need AI training
• Regulatory frameworks must adapt

RECOMMENDATIONS:
1. Invest in AI training for medical staff
2. Establish clear ethical guidelines
3. Start with diagnostic applications
4. Ensure robust data privacy measures

CONCLUSION:
AI represents a transformative opportunity for healthcare...
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

## 🚧 Extending NemoClaw

### Adding New Agents

1. Create a new agent class:
```python
from agents.base_agent import BaseAgent

class ValidatorAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="validator",
            role="Content Validator",
            goal="Validate accuracy and completeness",
            backstory="Expert validator...",
            **kwargs
        )
    
    def create_prompt(self, task, context):
        # Custom prompt logic
        return f"Validate: {task}"
```

2. Add to orchestrator workflow:
```python
self.validator = ValidatorAgent(model=model)
self.agents = [self.summarizer, self.analyzer, self.validator]
```

### Custom Workflows

Create conditional or parallel workflows:
```python
# Conditional execution
if len(text) > 1000:
    # Use detailed analysis
    analyzer = DetailedAnalyzer()
else:
    # Use quick analysis
    analyzer = QuickAnalyzer()

# Parallel execution (future enhancement)
results = []
for agent in [agent1, agent2, agent3]:
    result = agent.execute(task, context)
    results.append(result)
```

## 📊 Performance

Typical execution times (with Granite 4 Micro):
- **Summarizer**: 10-20 seconds
- **Analyzer**: 15-30 seconds
- **Total**: 25-50 seconds (~30-50 seconds average)

Performance depends on:
- Model size and speed
- Hardware (CPU/GPU)
- Text length and complexity
- Token limits

## 🔄 Comparison with OpenClaw

| Feature | OpenClaw | NemoClaw |
|---------|----------|----------|
| **Agents** | 3 (Planner, Researcher, Writer) | 2 (Summarizer, Analyzer) |
| **Use Case** | Research & Report Writing | Text Analysis |
| **Complexity** | High (multi-step research) | Low (direct analysis) |
| **Execution Time** | 80-160 seconds | 30-60 seconds |
| **Token Usage** | 800/1500/2000 | 600/800 |
| **Best For** | Academic research, comprehensive reports | Content analysis, quick insights |

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Parallel agent execution
- Streaming output support
- Additional agent types (sentiment, fact-checking, etc.)
- Tool integration (web search, file operations)
- Performance optimizations
- Error recovery mechanisms

## 📝 License

This project is created for educational purposes to demonstrate simple multi-agent orchestration patterns.

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.ai) for local LLM inference
- Powered by IBM's [Granite 4 Micro](https://www.ibm.com/granite) model
- Inspired by frameworks like CrewAI and LangGraph
- Simplified from the OpenClaw framework

---

**Made with Bob** 🤖

For questions or issues, please refer to the QUICKSTART.md guide or check the troubleshooting section above.