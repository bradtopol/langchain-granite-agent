#!/usr/bin/env python3
"""
Writer Agent for OpenClaw Orchestration
Synthesizes research into a comprehensive final report
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class WriterAgent(BaseAgent):
    """Agent responsible for writing the final research report"""
    
    def __init__(
        self,
        model: str = "granite4:micro",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7  # Higher temperature for more engaging writing
    ):
        """Initialize the Writer Agent"""
        super().__init__(
            name="writer",
            role="Research Writer",
            goal="Synthesize research findings into a comprehensive, well-structured report",
            backstory="""You are an accomplished research writer with a talent for 
            transforming complex information into clear, engaging narratives. You excel 
            at organizing ideas logically, maintaining coherent flow, and presenting 
            information in an accessible yet professional manner. Your reports are 
            comprehensive, well-structured, and insightful.""",
            model=model,
            base_url=base_url,
            temperature=temperature,
            max_tokens=2000
        )
    
    def create_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """
        Create a writing prompt
        
        Args:
            task: The research topic
            context: Shared context including plan and research findings
            
        Returns:
            Formatted prompt for writing
        """
        # Get previous outputs from context
        plan = context.get("planner", "No plan available")
        research = context.get("researcher", "No research available")
        
        prompt = f"""You are a {self.role}. {self.backstory}

Your goal: {self.goal}

Original Research Topic: {task}

Research Plan:
{plan}

Research Findings:
{research}

Based on the research plan and findings above, write a comprehensive research report.

Your report should include:

1. EXECUTIVE SUMMARY
   - Brief overview of the topic and key findings (2-3 paragraphs)

2. INTRODUCTION
   - Background and context
   - Importance of the topic
   - Scope of the research

3. MAIN FINDINGS
   - Organized by subtasks from the research plan
   - Each section should synthesize the research findings
   - Include relevant examples and evidence
   - Maintain logical flow between sections

4. ANALYSIS & INSIGHTS
   - Connections between different findings
   - Patterns and trends identified
   - Implications and significance

5. CONCLUSION
   - Summary of key takeaways
   - Future directions or recommendations
   - Final thoughts

Format your response as a professional research report with clear headings and well-organized content.
Write in a clear, engaging style that is both informative and accessible.
Ensure smooth transitions between sections and maintain a coherent narrative throughout.

Begin your report now:"""

        return prompt


# Made with Bob