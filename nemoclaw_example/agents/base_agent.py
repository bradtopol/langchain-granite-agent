#!/usr/bin/env python3
"""
Base Agent Class for NemoClaw Orchestration
Provides common functionality for all specialized agents
"""

import json
import sys
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

try:
    import requests
except ImportError:
    print("Error: 'requests' module not installed")
    print("Please install: pip install requests")
    sys.exit(1)


class BaseAgent(ABC):
    """Base class for all NemoClaw agents"""
    
    def __init__(
        self,
        name: str,
        role: str,
        goal: str,
        backstory: str,
        model: str = "granite4:micro",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        max_tokens: int = 800
    ):
        """
        Initialize a base agent
        
        Args:
            name: Agent's unique identifier
            role: Agent's role in the system
            goal: Agent's primary objective
            backstory: Agent's background and expertise
            model: LLM model to use
            base_url: Ollama API base URL
            temperature: Model temperature (higher = more creative)
            max_tokens: Maximum tokens to generate
        """
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    @abstractmethod
    def create_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """
        Create a prompt for the agent's specific task
        Must be implemented by subclasses
        
        Args:
            task: The task description
            context: Shared context from previous agents
            
        Returns:
            Formatted prompt string
        """
        pass
    
    def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task
        
        Args:
            task: Task description
            context: Shared context from orchestrator
            
        Returns:
            Dictionary with success status and output
        """
        print(f"\n{'='*70}")
        print(f"🤖 {self.name} ({self.role})")
        print(f"{'='*70}")
        print(f"Goal: {self.goal}")
        print(f"{'-'*70}\n")
        
        try:
            # Create the prompt
            prompt = self.create_prompt(task, context)
            
            # Call the LLM
            print(f"💭 Thinking...")
            response = self._call_llm(prompt)
            
            if response["success"]:
                output = response["output"]
                print(f"\n✓ Completed\n")
                print(f"{'-'*70}")
                print(output)
                print(f"{'-'*70}\n")
                
                return {
                    "success": True,
                    "output": output,
                    "metadata": {
                        "model": self.model,
                        "temperature": self.temperature
                    }
                }
            else:
                error_msg = response.get("error", "Unknown error")
                print(f"\n✗ Error: {error_msg}\n")
                return {
                    "success": False,
                    "output": "",
                    "error": error_msg
                }
                
        except Exception as e:
            error_msg = f"Agent execution failed: {str(e)}"
            print(f"\n✗ {error_msg}\n")
            return {
                "success": False,
                "output": "",
                "error": error_msg
            }
    
    def _call_llm(self, prompt: str) -> Dict[str, Any]:
        """
        Call the LLM with the given prompt
        
        Args:
            prompt: Prompt to send to the model
            
        Returns:
            Dictionary with success status and output
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "output": data.get("response", "").strip()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def __str__(self) -> str:
        return f"{self.name} ({self.role})"
    
    def __repr__(self) -> str:
        return f"BaseAgent(name='{self.name}', role='{self.role}')"


# Made with Bob