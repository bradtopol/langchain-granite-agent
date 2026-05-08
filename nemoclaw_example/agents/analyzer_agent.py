#!/usr/bin/env python3
"""
Analyzer Agent for NemoClaw Orchestration
Provides insights, patterns, and recommendations based on summarized content
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class AnalyzerAgent(BaseAgent):
    """Agent responsible for analyzing content and providing insights"""
    
    def __init__(
        self,
        model: str = "granite4:micro",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7  # Higher temperature for more creative analysis
    ):
        """Initialize the Analyzer Agent"""
        super().__init__(
            name="analyzer",
            role="Content Analyst",
            goal="Provide deep insights, identify patterns, and offer actionable recommendations",
            backstory="""You are a skilled analyst with expertise in critical thinking 
            and pattern recognition. You excel at seeing connections, identifying 
            implications, and providing actionable insights. Your analysis is thorough, 
            thoughtful, and practical, helping readers understand not just what the 
            content says, but what it means and why it matters.""",
            model=model,
            base_url=base_url,
            temperature=temperature,
            max_tokens=800
        )
    
    def create_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """
        Create an analysis prompt
        
        Args:
            task: The original text
            context: Shared context including the summary
            
        Returns:
            Formatted prompt for analysis
        """
        # Get the summary from context
        summary = context.get("summarizer", "No summary available")
        
        prompt = f"""You are a {self.role}. {self.backstory}

Your goal: {self.goal}

ORIGINAL TEXT:
{task}

SUMMARY FROM SUMMARIZER:
{summary}

Based on the original text and the summary above, provide a comprehensive analysis.

Your analysis should include:

1. KEY INSIGHTS (3-5 insights)
   - What are the deeper meanings or implications?
   - What stands out as particularly important or interesting?
   - What might not be immediately obvious?

2. PATTERNS & TRENDS (2-4 patterns)
   - What patterns, trends, or connections do you notice?
   - Are there recurring themes or ideas?
   - How do different parts relate to each other?

3. IMPLICATIONS (2-3 implications)
   - What are the broader implications of this content?
   - Why does this matter?
   - What impact might this have?

4. RECOMMENDATIONS (3-5 recommendations)
   - What actions or next steps would you suggest?
   - What should readers pay attention to?
   - What questions should be explored further?

5. CONCLUSION (1-2 paragraphs)
   - Synthesize your analysis
   - Provide final thoughts on the significance of this content

Format your response as follows:

KEY INSIGHTS:
• [Insight 1]
• [Insight 2]
• [Insight 3]
[Continue as needed]

PATTERNS & TRENDS:
• [Pattern 1]
• [Pattern 2]
[Continue as needed]

IMPLICATIONS:
• [Implication 1]
• [Implication 2]
[Continue as needed]

RECOMMENDATIONS:
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]
[Continue as needed]

CONCLUSION:
[1-2 paragraph synthesis and final thoughts]

Be thoughtful, insightful, and practical. Focus on providing value through your analysis."""

        return prompt


# Made with Bob