#!/usr/bin/env python3
"""
Researcher Agent for OpenClaw Orchestration
Gathers information and conducts research on subtasks
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    """Agent responsible for conducting research and gathering information"""
    
    def __init__(
        self,
        model: str = "granite4:micro",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.6  # Balanced temperature for factual yet comprehensive research
    ):
        """Initialize the Researcher Agent"""
        super().__init__(
            name="researcher",
            role="Research Specialist",
            goal="Conduct thorough research on each subtask and gather relevant information",
            backstory="""You are a meticulous research specialist with expertise across 
            multiple domains. You excel at finding relevant information, synthesizing 
            knowledge from various sources, and presenting findings in a clear, organized 
            manner. You always cite key facts and provide comprehensive coverage of topics.""",
            model=model,
            base_url=base_url,
            temperature=temperature,
            max_tokens=1500
        )
    
    def create_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """
        Create a research prompt
        
        Args:
            task: The research topic
            context: Shared context including the research plan
            
        Returns:
            Formatted prompt for research
        """
        # Get the research plan from context
        plan = context.get("planner", "No plan available")
        
        prompt = f"""You are a {self.role}. {self.backstory}

Your goal: {self.goal}

Original Research Topic: {task}

Research Plan from Planner:
{plan}

Based on the research plan above, conduct comprehensive research on each subtask.
For each subtask identified in the plan, provide:

1. KEY FINDINGS: Main discoveries and important facts
2. DETAILED INFORMATION: In-depth explanation and context
3. RELEVANT EXAMPLES: Concrete examples or case studies
4. CURRENT STATE: Latest developments or current understanding
5. IMPLICATIONS: Why this matters and its significance

Format your response as:

RESEARCH FINDINGS

SUBTASK 1: [Title from plan]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Key Findings:
• [Finding 1]
• [Finding 2]
• [Finding 3]

Detailed Information:
[Comprehensive explanation with context and background]

Relevant Examples:
[Concrete examples or case studies]

Current State:
[Latest developments and current understanding]

Implications:
[Why this matters and its significance]

SUBTASK 2: [Title from plan]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Continue for each subtask]

SYNTHESIS:
[Brief overview of how all findings connect and what they reveal about the overall topic]

Provide thorough, accurate, and well-organized research findings. Be specific and informative."""

        return prompt


# Made with Bob