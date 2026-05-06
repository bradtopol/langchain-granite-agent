#!/usr/bin/env python3
"""
Planner Agent for OpenClaw Orchestration
Breaks down research topics into actionable subtasks
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    """Agent responsible for strategic planning and task decomposition"""
    
    def __init__(
        self,
        model: str = "granite4:micro",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.5  # Lower temperature for more structured planning
    ):
        """Initialize the Planner Agent"""
        super().__init__(
            name="planner",
            role="Strategic Planner",
            goal="Break down research topics into clear, actionable subtasks",
            backstory="""You are an expert research strategist with years of experience 
            in academic and professional research. You excel at analyzing complex topics 
            and breaking them down into logical, manageable components. Your plans are 
            clear, comprehensive, and actionable.""",
            model=model,
            base_url=base_url,
            temperature=temperature,
            max_tokens=800
        )
    
    def create_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """
        Create a planning prompt
        
        Args:
            task: The research topic to plan for
            context: Shared context (not used by planner as it's first)
            
        Returns:
            Formatted prompt for planning
        """
        prompt = f"""You are a {self.role}. {self.backstory}

Your goal: {self.goal}

Research Topic: {task}

Please create a comprehensive research plan by breaking down this topic into 3-5 specific subtasks.
For each subtask, provide:
1. A clear, focused research question or objective
2. Key areas to investigate
3. Expected outcomes

Format your response as follows:

RESEARCH PLAN: [Topic Name]

SUBTASK 1: [Title]
- Research Question: [Specific question to answer]
- Key Areas: [What to investigate]
- Expected Outcome: [What we should learn]

SUBTASK 2: [Title]
- Research Question: [Specific question to answer]
- Key Areas: [What to investigate]
- Expected Outcome: [What we should learn]

[Continue for 3-5 subtasks]

OVERALL APPROACH:
[Brief description of how these subtasks work together]

Be specific, actionable, and comprehensive. Each subtask should be independently researchable."""

        return prompt


# Made with Bob