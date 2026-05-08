# NemoClaw Quick Start Guide

Get up and running with NemoClaw in 5 minutes!

## 📋 Prerequisites Checklist

- [ ] Python 3.8 or higher installed
- [ ] Ollama installed and running
- [ ] Granite 4 Micro model downloaded

## 🚀 Installation Steps

### Step 1: Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai
```

### Step 2: Start Ollama Server

```bash
# Start the Ollama server (in a separate terminal)
ollama serve
```

### Step 3: Pull Granite 4 Micro Model

```bash
# Download the model (this may take a few minutes)
ollama pull granite4:micro

# Verify installation
ollama list
```

### Step 4: Install Python Dependencies

```bash
# Navigate to nemoclaw_example directory
cd nemoclaw_example

# Install required packages
pip install -r requirements.txt
```

## 🎯 Running Your First Analysis

### Option 1: Interactive Mode (Recommended for First Time)

```bash
# Run the interactive mode
./run_nemoclaw.sh

# Or use Python directly
python3 example_analysis.py interactive
```

**What to expect:**
1. You'll see agent information displayed
2. Enter any text you want to analyze
3. Watch as the Summarizer extracts key points
4. See the Analyzer provide insights and recommendations
5. Get a complete analysis report

**Tips for Interactive Mode:**
- Type `paste` to enter multi-line text
- End multi-line input with `END` on a new line
- Type `quit` to exit

### Option 2: Run Pre-built Examples

```bash
# Example 1: AI in Healthcare
./run_nemoclaw.sh example1

# Example 2: Climate Change
./run_nemoclaw.sh example2

# Example 3: Remote Work
./run_nemoclaw.sh example3
```

## 📝 Your First Custom Analysis

Create a file called `my_analysis.py`:

```python
from orchestrator import NemoClawOrchestrator

# Initialize the orchestrator
orchestrator = NemoClawOrchestrator(model="granite4:micro")

# Your text to analyze
text = """
Artificial intelligence is transforming how we work and live.
Machine learning algorithms can now perform tasks that once
required human intelligence, from recognizing images to
understanding natural language. This technology is being
applied across industries, from healthcare to finance,
creating both opportunities and challenges for society.
"""

# Run the analysis
result = orchestrator.analyze_text(text)

# Display results
if result.success:
    print("\n=== SUMMARY ===")
    print(result.summary)
    
    print("\n=== ANALYSIS ===")
    print(result.analysis)
    
    print(f"\n✓ Completed in {result.execution_time:.2f}s")
else:
    print(f"❌ Error: {result.error}")
```

Run it:
```bash
python3 my_analysis.py
```

## 🔍 Understanding the Output

### Summarizer Output Structure
```
KEY POINTS:
• Main point 1
• Main point 2
• Main point 3

MAIN THEMES:
• Theme 1
• Theme 2

SUMMARY:
[2-3 paragraph summary]
```

### Analyzer Output Structure
```
KEY INSIGHTS:
• Insight 1
• Insight 2

PATTERNS & TRENDS:
• Pattern 1
• Pattern 2

IMPLICATIONS:
• Implication 1
• Implication 2

RECOMMENDATIONS:
1. Recommendation 1
2. Recommendation 2

CONCLUSION:
[Final synthesis]
```

## ⚙️ Common Configurations

### Use a Different Model

```python
# Use Llama 2
orchestrator = NemoClawOrchestrator(model="llama2")

# Use Mistral
orchestrator = NemoClawOrchestrator(model="mistral")

# Use Granite 3 Dense
orchestrator = NemoClawOrchestrator(model="granite3-dense:2b")
```

### Adjust Agent Temperature

```python
from agents import SummarizerAgent, AnalyzerAgent

# More creative summarizer
summarizer = SummarizerAgent(temperature=0.7)

# More focused analyzer
analyzer = AnalyzerAgent(temperature=0.5)
```

### Disable Verbose Output

```python
# Quiet mode - only show final results
orchestrator = NemoClawOrchestrator(verbose=False)
```

## 🐛 Troubleshooting

### Problem: "Cannot connect to Ollama server"

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### Problem: "Model not found"

**Solution:**
```bash
# Pull the model
ollama pull granite4:micro

# Verify it's installed
ollama list
```

### Problem: "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install requests typing-extensions
```

### Problem: Analysis takes too long

**Possible causes:**
- Large text input (try shorter text)
- Slow hardware (consider using a smaller model)
- High token limits (adjust in agent configuration)

**Solution:**
```python
# Use shorter max_tokens
from agents import SummarizerAgent, AnalyzerAgent

summarizer = SummarizerAgent(max_tokens=400)
analyzer = AnalyzerAgent(max_tokens=500)
```

### Problem: Poor quality results

**Solution:**
```python
# Adjust temperature for better results
# Lower = more focused, Higher = more creative

# For factual content
summarizer = SummarizerAgent(temperature=0.3)
analyzer = AnalyzerAgent(temperature=0.5)

# For creative content
summarizer = SummarizerAgent(temperature=0.6)
analyzer = AnalyzerAgent(temperature=0.8)
```

## 📚 Next Steps

1. **Explore Examples**: Run all three pre-built examples to see different use cases
2. **Try Your Own Text**: Use interactive mode with your own content
3. **Customize Agents**: Experiment with different temperatures and models
4. **Read Full Documentation**: Check out README.md for advanced features
5. **Extend the Framework**: Add your own agents or modify existing ones

## 💡 Tips for Best Results

1. **Text Length**: 200-1000 words works best
2. **Clear Content**: Well-structured text produces better analysis
3. **Specific Topics**: Focused content yields more actionable insights
4. **Model Selection**: Granite 4 Micro is fast and efficient for most tasks
5. **Temperature Tuning**: Start with defaults, adjust based on results

## 🎓 Learning Resources

- **Architecture**: See README.md for detailed architecture diagrams
- **Code Examples**: Check `example_analysis.py` for usage patterns
- **Agent Design**: Review agent files in `agents/` directory
- **Orchestration**: Study `orchestrator.py` for workflow logic

## 🆘 Getting Help

If you encounter issues:

1. Check the Troubleshooting section above
2. Review the full README.md documentation
3. Verify all prerequisites are met
4. Check Ollama logs: `ollama logs`
5. Test with a simple example first

## ✅ Quick Verification

Run this to verify everything is working:

```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Test Python imports
python3 -c "from orchestrator import NemoClawOrchestrator; print('✓ Imports OK')"

# Run a quick example
./run_nemoclaw.sh example1
```

If all three succeed, you're ready to go! 🎉

---

**Made with Bob** 🤖

Happy analyzing! For more details, see the full [README.md](README.md).