#!/usr/bin/env python3
"""
LangChain ReAct Agent with Granite 4 Micro
A demonstration of the ReAct (Reasoning and Acting) pattern using IBM's Granite 4 micro model
"""

import sys
from pathlib import Path
from typing import List, Optional

# Check for required dependencies
try:
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain_ollama import ChatOllama
    from langchain.prompts import PromptTemplate
    from langchain.tools import Tool
except ImportError as e:
    print(f"Error: Required LangChain packages not installed: {e}")
    print("\nPlease install dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

# Import custom tools
from tools.calculator import CalculatorTool
from tools.file_operations import FileOperationsTool
from tools.web_search import WebSearchTool


class GraniteReActAgent:
    """
    ReAct Agent using Granite 4 micro model via Ollama
    
    The ReAct pattern combines reasoning and acting:
    1. Thought: Agent reasons about what to do
    2. Action: Agent selects and uses a tool
    3. Observation: Agent observes the tool's output
    4. Repeat until task is complete
    5. Final Answer: Provide result to user
    """
    
    def __init__(
        self,
        model: str = "granite4:micro",
        temperature: float = 0.1,
        workspace_dir: str = "workspace",
        max_iterations: int = 10,
        verbose: bool = True
    ):
        """
        Initialize the ReAct agent
        
        Args:
            model: Ollama model name (default: granite4:micro)
            temperature: Model temperature for consistency (default: 0.1)
            workspace_dir: Directory for file operations
            max_iterations: Maximum reasoning iterations
            verbose: Print intermediate steps
        """
        self.model_name = model
        self.temperature = temperature
        self.workspace_dir = Path(workspace_dir)
        self.max_iterations = max_iterations
        self.verbose = verbose
        
        # Ensure workspace exists
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize the LLM
        self.llm = self._initialize_llm()
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Create the agent
        self.agent_executor = self._create_agent()
    
    def _initialize_llm(self) -> ChatOllama:
        """Initialize the Granite 4 micro model via Ollama"""
        try:
            llm = ChatOllama(
                model=self.model_name,
                temperature=self.temperature,
                base_url="http://localhost:11434"
            )
            return llm
        except Exception as e:
            print(f"Error initializing Ollama: {e}")
            print("\nMake sure:")
            print("1. Ollama is installed and running (ollama serve)")
            print(f"2. The {self.model_name} model is available (ollama pull {self.model_name})")
            sys.exit(1)
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize the custom tools for the agent"""
        # Create tool instances
        calculator = CalculatorTool()
        file_ops = FileOperationsTool(workspace_dir=str(self.workspace_dir))
        web_search = WebSearchTool(max_results=5)
        
        # Wrap them as LangChain Tools
        tools = [
            Tool(
                name=calculator.name,
                func=calculator._run,
                description=calculator.description
            ),
            Tool(
                name=file_ops.name,
                func=file_ops._run,
                description=file_ops.description
            ),
            Tool(
                name=web_search.name,
                func=web_search._run,
                description=web_search.description
            )
        ]
        
        return tools
    
    def _create_agent(self) -> AgentExecutor:
        """Create the ReAct agent with custom prompt"""
        
        # Custom ReAct prompt template
        template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
        
        prompt = PromptTemplate.from_template(template)
        
        # Create the ReAct agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.verbose,
            max_iterations=self.max_iterations,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        
        return agent_executor
    
    def run(self, query: str) -> dict:
        """
        Run the agent with a query
        
        Args:
            query: User's question or task
            
        Returns:
            Dictionary with output and intermediate steps
        """
        try:
            result = self.agent_executor.invoke({"input": query})
            return result
        except Exception as e:
            return {
                "output": f"Error: {str(e)}",
                "intermediate_steps": []
            }
    
    def run_simple(self, query: str) -> str:
        """
        Run the agent and return just the final answer
        
        Args:
            query: User's question or task
            
        Returns:
            Final answer string
        """
        result = self.run(query)
        return result.get("output", "No output generated")
    
    def get_tool_names(self) -> List[str]:
        """Get list of available tool names"""
        return [tool.name for tool in self.tools]
    
    def get_tool_descriptions(self) -> dict:
        """Get dictionary of tool names and descriptions"""
        return {tool.name: tool.description for tool in self.tools}


def main():
    """Main function to demonstrate the ReAct agent"""
    print("=" * 70)
    print("LangChain ReAct Agent with Granite 4 Micro")
    print("=" * 70)
    print()
    
    # Initialize the agent
    print("Initializing agent...")
    agent = GraniteReActAgent(
        model="granite4:micro",
        temperature=0.1,
        workspace_dir="workspace",
        verbose=True
    )
    
    print("✓ Agent initialized successfully")
    print()
    print("Available tools:")
    for name, desc in agent.get_tool_descriptions().items():
        print(f"  • {name}")
    print()
    print("=" * 70)
    print()
    
    # Interactive mode
    print("Enter your questions or tasks (type 'quit' to exit)")
    print("Examples:")
    print("  - Calculate 15% of 240 and multiply by 3")
    print("  - Search for LangChain documentation and summarize")
    print("  - Create a file with a list of programming languages")
    print()
    
    while True:
        try:
            query = input("You: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break
            
            print("\n" + "=" * 70)
            print("Agent working...")
            print("=" * 70)
            print()
            
            # Run the agent
            result = agent.run_simple(query)
            
            print("\n" + "=" * 70)
            print("Final Answer:")
            print("=" * 70)
            print(result)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()

# Made with Bob