#!/usr/bin/env python3
"""
Summarizer Agent for NemoClaw Orchestration
Extracts key points and creates concise summaries from text
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class SummarizerAgent(BaseAgent):
    """Agent responsible for summarizing text and extracting key points"""
    
    def __init__(
        self,
        model: str = "granite4:micro",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.5  # Lower temperature for structured output
    ):
        """Initialize the Summarizer Agent"""
        super().__init__(
            name="summarizer",
            role="Text Summarizer",
            goal="Extract key points and create concise, accurate summaries",
            backstory="""You are an expert at distilling complex information into 
            clear, concise summaries. You excel at identifying the most important 
            points, themes, and takeaways from any text. Your summaries are accurate, 
            well-organized, and capture the essence of the content.""",
            model=model,
            base_url=base_url,
            temperature=temperature,
            max_tokens=600
        )
    
    def create_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """
        Create a summarization prompt
        
        Args:
            task: The text to summarize
            context: Shared context (not used by summarizer as it's first)
            
        Returns:
            Formatted prompt for summarization
        """
        prompt = f"""You are a {self.role}. {self.backstory}

Your goal: {self.goal}

TEXT TO ANALYZE:
{task}

Please analyze the text above and provide:

1. KEY POINTS (3-7 bullet points)
   - Extract the most important facts, ideas, or arguments
   - Each point should be clear and concise
   - Focus on substance, not style

2. MAIN THEMES (2-4 themes)
   - Identify overarching themes or topics
   - What are the central ideas?

3. BRIEF SUMMARY (2-3 paragraphs)
   - Provide a concise overview of the content
   - Capture the essence and main message
   - Be accurate and objective

Format your response as follows:

KEY POINTS:
• [Point 1]
• [Point 2]
• [Point 3]
[Continue as needed]

MAIN THEMES:
• [Theme 1]
• [Theme 2]
[Continue as needed]

SUMMARY:
[2-3 paragraph summary that captures the essence of the text]

Be clear, concise, and accurate. Focus on the most important information."""

        return prompt


# Made with Bob