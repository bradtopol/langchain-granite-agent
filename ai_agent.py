#!/usr/bin/env python3
"""
Simple AI Agent with conversational capabilities
"""

import re
from datetime import datetime
from typing import Dict, List, Callable


class SimpleAIAgent:
    """A simple rule-based AI agent that can respond to user queries"""
    
    def __init__(self, name: str = "Bob"):
        self.name = name
        self.conversation_history: List[Dict[str, str]] = []
        self.knowledge_base = {
            "greeting": ["hello", "hi", "hey", "greetings"],
            "farewell": ["bye", "goodbye", "see you", "farewell"],
            "time": ["time", "what time", "current time"],
            "date": ["date", "what date", "today"],
            "help": ["help", "what can you do", "capabilities"],
            "name": ["your name", "who are you", "what's your name"],
        }
        
        # Map intents to handler functions
        self.intent_handlers: Dict[str, Callable] = {
            "greeting": self._handle_greeting,
            "farewell": self._handle_farewell,
            "time": self._handle_time,
            "date": self._handle_date,
            "help": self._handle_help,
            "name": self._handle_name,
        }
    
    def _detect_intent(self, user_input: str) -> str:
        """Detect the intent of the user's input"""
        user_input_lower = user_input.lower()
        
        for intent, keywords in self.knowledge_base.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    return intent
        
        return "unknown"
    
    def _handle_greeting(self, user_input: str) -> str:
        """Handle greeting intents"""
        return f"Hello! I'm {self.name}, your AI assistant. How can I help you today?"
    
    def _handle_farewell(self, user_input: str) -> str:
        """Handle farewell intents"""
        return f"Goodbye! It was nice talking to you. Have a great day!"
    
    def _handle_time(self, user_input: str) -> str:
        """Handle time-related queries"""
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    
    def _handle_date(self, user_input: str) -> str:
        """Handle date-related queries"""
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {current_date}."
    
    def _handle_help(self, user_input: str) -> str:
        """Handle help requests"""
        capabilities = [
            "- Greet you and have a conversation",
            "- Tell you the current time",
            "- Tell you today's date",
            "- Answer questions about myself",
            "- Provide general assistance"
        ]
        return f"I can help you with:\n" + "\n".join(capabilities)
    
    def _handle_name(self, user_input: str) -> str:
        """Handle name-related queries"""
        return f"I'm {self.name}, a simple AI agent designed to assist you with basic tasks and conversations."
    
    def _handle_unknown(self, user_input: str) -> str:
        """Handle unknown intents"""
        return (
            "I'm not sure I understand that. I'm a simple AI agent with limited capabilities. "
            "Try asking me about the time, date, or type 'help' to see what I can do."
        )
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate a response"""
        # Store in conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Detect intent
        intent = self._detect_intent(user_input)
        
        # Generate response based on intent
        if intent in self.intent_handlers:
            response = self.intent_handlers[intent](user_input)
        else:
            response = self._handle_unknown(user_input)
        
        # Store response in conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Return the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []


def main():
    """Main function to run the AI agent in interactive mode"""
    agent = SimpleAIAgent(name="Bob")
    
    print("=" * 60)
    print(f"Welcome! I'm {agent.name}, your AI assistant.")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("=" * 60)
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit"]:
                print(f"\n{agent.name}: Goodbye! Have a great day!")
                break
            
            response = agent.process_input(user_input)
            print(f"{agent.name}: {response}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{agent.name}: Goodbye! Have a great day!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

# Made with Bob