#!/usr/bin/env python3
"""
Data Models for OpenClaw Orchestration
Defines Task, Context, and Result structures for agent communication
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class Task:
    """Represents a task to be executed by an agent"""
    description: str
    agent_name: str
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        return f"Task(agent={self.agent_name}, desc={self.description[:50]}...)"


@dataclass
class AgentResult:
    """Standardized result from an agent execution"""
    agent_name: str
    success: bool
    output: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __str__(self) -> str:
        status = "✓" if self.success else "✗"
        return f"{status} {self.agent_name}: {self.output[:100]}..."


@dataclass
class Context:
    """Shared context passed between agents during orchestration"""
    original_request: str
    current_step: str = ""
    results: Dict[str, AgentResult] = field(default_factory=dict)
    shared_data: Dict[str, Any] = field(default_factory=dict)
    
    def add_result(self, agent_name: str, result: AgentResult):
        """Add an agent's result to the context"""
        self.results[agent_name] = result
        self.shared_data[agent_name] = result.output
    
    def get_result(self, agent_name: str) -> Optional[AgentResult]:
        """Get a specific agent's result"""
        return self.results.get(agent_name)
    
    def get_all_outputs(self) -> str:
        """Get all agent outputs as a formatted string"""
        outputs = []
        for agent_name, result in self.results.items():
            outputs.append(f"=== {agent_name} ===\n{result.output}\n")
        return "\n".join(outputs)
    
    def __str__(self) -> str:
        return f"Context(request={self.original_request[:50]}..., steps={len(self.results)})"


@dataclass
class OrchestrationResult:
    """Final result from the orchestration process"""
    success: bool
    context: Context
    final_output: str
    execution_time: float
    error: Optional[str] = None
    
    @property
    def plan(self) -> str:
        """Get the planner's output"""
        result = self.context.get_result("planner")
        return result.output if result else ""
    
    @property
    def research(self) -> str:
        """Get the researcher's output"""
        result = self.context.get_result("researcher")
        return result.output if result else ""
    
    @property
    def report(self) -> str:
        """Get the writer's output (final report)"""
        result = self.context.get_result("writer")
        return result.output if result else ""
    
    def __str__(self) -> str:
        status = "✓ Success" if self.success else "✗ Failed"
        return f"OrchestrationResult({status}, time={self.execution_time:.2f}s)"


# Made with Bob