#!/usr/bin/env python3
"""
Example workflows for LangChain ReAct Agent with Granite 4 Micro
Demonstrates various agent capabilities and multi-step reasoning
"""

import sys
from langchain_react_agent import GraniteReActAgent


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def run_example(agent: GraniteReActAgent, title: str, query: str):
    """Run a single example and display results"""
    print_section(title)
    print(f"Query: {query}\n")
    print("-" * 70)
    
    try:
        result = agent.run_simple(query)
        print(f"\nFinal Answer:\n{result}\n")
    except Exception as e:
        print(f"\nError: {e}\n")


def main():
    """Run example workflows"""
    print("=" * 70)
    print("LangChain ReAct Agent - Example Workflows")
    print("Demonstrating Granite 4 Micro with Multi-Step Reasoning")
    print("=" * 70)
    
    # Initialize the agent
    print("\nInitializing agent...")
    try:
        agent = GraniteReActAgent(
            model="granite4:micro",
            temperature=0.1,
            workspace_dir="workspace",
            verbose=True  # Show reasoning steps
        )
        print("✓ Agent initialized successfully\n")
    except Exception as e:
        print(f"Error initializing agent: {e}")
        print("\nMake sure:")
        print("1. Ollama is running (ollama serve)")
        print("2. Granite 4 micro is installed (ollama pull granite4:micro)")
        print("3. Dependencies are installed (pip install -r requirements.txt)")
        sys.exit(1)
    
    # Example 1: Simple Calculator
    run_example(
        agent,
        "Example 1: Simple Mathematical Calculation",
        "What is 15% of 240?"
    )
    
    # Example 2: Multi-step Calculation
    run_example(
        agent,
        "Example 2: Multi-Step Mathematical Reasoning",
        "Calculate 15% of 240, then multiply that result by 3, and tell me the final answer."
    )
    
    # Example 3: File Operations
    run_example(
        agent,
        "Example 3: File Creation",
        "Create a file called programming_languages.txt with a list of 5 popular programming languages."
    )
    
    # Example 4: File Read
    run_example(
        agent,
        "Example 4: File Reading",
        "Read the contents of programming_languages.txt and tell me what's in it."
    )
    
    # Example 5: Web Search
    run_example(
        agent,
        "Example 5: Web Search",
        "Search for information about LangChain framework and give me a brief summary."
    )
    
    # Example 6: Complex Multi-Tool Workflow
    run_example(
        agent,
        "Example 6: Complex Multi-Tool Workflow",
        "Search for the latest Python version, calculate what 25% of 100 is, and create a file called results.txt with both pieces of information."
    )
    
    # Example 7: File Listing
    run_example(
        agent,
        "Example 7: List Workspace Files",
        "List all files in the workspace directory and tell me how many files there are."
    )
    
    # Example 8: Mathematical Expression
    run_example(
        agent,
        "Example 8: Complex Mathematical Expression",
        "Calculate the square root of 144, add 10 to it, and then multiply by 2."
    )
    
    # Summary
    print_section("Examples Complete")
    print("All example workflows have been executed.")
    print("\nThe agent demonstrated:")
    print("  ✓ Mathematical calculations")
    print("  ✓ Multi-step reasoning")
    print("  ✓ File operations (create, read, list)")
    print("  ✓ Web search capabilities")
    print("  ✓ Complex multi-tool workflows")
    print("\nCheck the 'workspace' directory for created files.")
    print()


if __name__ == "__main__":
    main()

# Made with Bob