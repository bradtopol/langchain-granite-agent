#!/usr/bin/env python3
"""
NemoClaw Orchestrator
Coordinates two agents (Summarizer and Analyzer) to process and analyze text
"""

import sys
import time
from typing import Optional, Dict, Any

from models import Context, AgentResult, OrchestrationResult
from agents import SummarizerAgent, AnalyzerAgent


class NemoClawOrchestrator:
    """
    Orchestrates two agents in a sequential workflow
    
    Workflow: Summarizer → Analyzer
    """
    
    def __init__(
        self,
        model: str = "granite4:micro",
        base_url: str = "http://localhost:11434",
        verbose: bool = True
    ):
        """
        Initialize the orchestrator
        
        Args:
            model: LLM model to use for all agents
            base_url: Ollama API base URL
            verbose: Whether to print detailed progress
        """
        self.model = model
        self.base_url = base_url
        self.verbose = verbose
        
        # Initialize agents
        self.summarizer = SummarizerAgent(model=model, base_url=base_url)
        self.analyzer = AnalyzerAgent(model=model, base_url=base_url)
        
        # Agent execution order
        self.agents = [self.summarizer, self.analyzer]
    
    def check_ollama_connection(self) -> bool:
        """Check if Ollama server is running"""
        if not self.summarizer.check_connection():
            print("❌ Error: Cannot connect to Ollama server")
            print("\nPlease make sure:")
            print("  1. Ollama is installed (https://ollama.ai)")
            print("  2. Ollama server is running: ollama serve")
            print(f"  3. Model is installed: ollama pull {self.model}")
            return False
        return True
    
    def analyze_text(self, text: str) -> OrchestrationResult:
        """
        Run the complete text analysis workflow
        
        Args:
            text: Text content to analyze
            
        Returns:
            OrchestrationResult with all outputs and metadata
        """
        start_time = time.time()
        
        print("\n" + "="*70)
        print("📊 NemoClaw Text Analysis Orchestration")
        print("="*70)
        print(f"\nText length: {len(text)} characters")
        print(f"Model: {self.model}")
        print(f"Agents: {len(self.agents)}")
        print("\n" + "="*70)
        
        # Check Ollama connection
        if not self.check_ollama_connection():
            return OrchestrationResult(
                success=False,
                context=Context(original_request=text),
                final_output="",
                execution_time=0,
                error="Cannot connect to Ollama server"
            )
        
        # Initialize context
        context = Context(original_request=text)
        
        # Execute agents sequentially
        for i, agent in enumerate(self.agents, 1):
            context.current_step = agent.name
            
            if self.verbose:
                print(f"\n{'='*70}")
                print(f"Step {i}/{len(self.agents)}: {agent.name.upper()}")
                print(f"{'='*70}")
            
            # Execute agent
            result_dict = agent.execute(
                task=text,
                context=context.shared_data
            )
            
            # Create AgentResult
            agent_result = AgentResult(
                agent_name=agent.name,
                success=result_dict["success"],
                output=result_dict.get("output", ""),
                metadata=result_dict.get("metadata", {})
            )
            
            # Check for failure
            if not agent_result.success:
                error_msg = result_dict.get("error", "Unknown error")
                print(f"\n❌ Agent {agent.name} failed: {error_msg}")
                
                execution_time = time.time() - start_time
                return OrchestrationResult(
                    success=False,
                    context=context,
                    final_output="",
                    execution_time=execution_time,
                    error=f"Agent {agent.name} failed: {error_msg}"
                )
            
            # Add result to context
            context.add_result(agent.name, agent_result)
            
            if self.verbose:
                print(f"\n✓ {agent.name} completed successfully")
        
        # Get final output (analyzer's output)
        analyzer_result = context.get_result("analyzer")
        final_output = analyzer_result.output if analyzer_result else ""
        
        execution_time = time.time() - start_time
        
        # Print summary
        print("\n" + "="*70)
        print("✅ ORCHESTRATION COMPLETE")
        print("="*70)
        print(f"Execution time: {execution_time:.2f}s")
        print(f"Agents executed: {len(context.results)}")
        print("="*70 + "\n")
        
        return OrchestrationResult(
            success=True,
            context=context,
            final_output=final_output,
            execution_time=execution_time
        )
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about all agents"""
        return {
            "agents": [
                {
                    "name": agent.name,
                    "role": agent.role,
                    "goal": agent.goal
                }
                for agent in self.agents
            ],
            "model": self.model,
            "workflow": " → ".join(agent.name for agent in self.agents)
        }
    
    def print_agent_info(self):
        """Print information about all agents"""
        print("\n" + "="*70)
        print("NemoClaw Orchestrator - Agent Information")
        print("="*70)
        print(f"\nModel: {self.model}")
        print(f"Workflow: {' → '.join(agent.name.title() for agent in self.agents)}")
        print("\nAgents:")
        
        for agent in self.agents:
            print(f"\n  {agent.name.upper()}")
            print(f"  Role: {agent.role}")
            print(f"  Goal: {agent.goal}")
            print(f"  Temperature: {agent.temperature}")
        
        print("\n" + "="*70 + "\n")


# Made with Bob