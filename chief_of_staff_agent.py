#!/usr/bin/env python3
"""
Chief of Staff Agent using Ollama
An intelligent assistant that helps manage tasks, coordinate activities, and provide strategic support
"""

import json
import sys
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' module is not installed.")
    print("\nPlease install it using:")
    print("  pip install requests")
    print("or")
    print("  pip install -r requirements.txt")
    sys.exit(1)


class ChiefOfStaffAgent:
    """Intelligent Chief of Staff agent using Ollama's Granite model"""
    
    def __init__(self, model: str = "granite3-dense:2b", base_url: str = "http://localhost:11434"):
        """
        Initialize the Chief of Staff agent
        
        Args:
            model: The Granite model to use (default: granite3-dense:2b)
            base_url: The Ollama API base URL
        """
        self.model = model
        self.base_url = base_url
        self.chat_url = f"{base_url}/api/chat"
        self.conversation_history: List[Dict[str, str]] = []
        self.tasks: List[Dict[str, Any]] = []
        self.notes: List[Dict[str, str]] = []
        self.decisions: List[Dict[str, Any]] = []
        
        # System prompt for the Chief of Staff agent
        self.system_prompt = """You are an intelligent Chief of Staff assistant. Your role is to:

1. **Task Management**: Help organize, prioritize, and track tasks and projects
2. **Strategic Planning**: Assist with decision-making and strategic thinking
3. **Communication**: Draft messages, summaries, and reports
4. **Coordination**: Help coordinate activities and manage schedules
5. **Analysis**: Provide insights and analysis on various topics
6. **Problem Solving**: Help break down complex problems into actionable steps

Your communication style should be:
- Professional yet approachable
- Clear and concise
- Action-oriented
- Strategic and thoughtful
- Proactive in identifying potential issues

When helping with tasks:
- Break down complex tasks into manageable steps
- Identify dependencies and priorities
- Suggest timelines and milestones
- Anticipate potential obstacles

When providing analysis:
- Consider multiple perspectives
- Identify key factors and trade-offs
- Provide data-driven insights when possible
- Offer clear recommendations

Always be helpful, efficient, and focused on enabling better decision-making and execution."""
    
    def check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def list_models(self) -> Optional[List[str]]:
        """List available models in Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error listing models: {e}")
            return None
    
    def add_task(self, title: str, description: str = "", priority: str = "medium") -> Dict[str, Any]:
        """
        Add a new task
        
        Args:
            title: Task title
            description: Task description
            priority: Task priority (low, medium, high)
            
        Returns:
            The created task
        """
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        self.tasks.append(task)
        return task
    
    def update_task_status(self, task_id: int, status: str) -> Optional[Dict[str, Any]]:
        """
        Update task status
        
        Args:
            task_id: Task ID
            status: New status (pending, in_progress, completed, cancelled)
            
        Returns:
            Updated task or None if not found
        """
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = status
                if status == "completed":
                    task["completed_at"] = datetime.now().isoformat()
                return task
        return None
    
    def get_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get tasks, optionally filtered by status
        
        Args:
            status: Filter by status (optional)
            
        Returns:
            List of tasks
        """
        if status:
            return [t for t in self.tasks if t["status"] == status]
        return self.tasks
    
    def add_note(self, content: str, category: str = "general") -> Dict[str, str]:
        """
        Add a note
        
        Args:
            content: Note content
            category: Note category
            
        Returns:
            The created note
        """
        note = {
            "id": len(self.notes) + 1,
            "content": content,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
        self.notes.append(note)
        return note
    
    def add_decision(self, title: str, context: str, options: List[str], 
                     recommendation: str = "") -> Dict[str, Any]:
        """
        Record a decision point
        
        Args:
            title: Decision title
            context: Decision context
            options: Available options
            recommendation: Recommended option
            
        Returns:
            The created decision record
        """
        decision = {
            "id": len(self.decisions) + 1,
            "title": title,
            "context": context,
            "options": options,
            "recommendation": recommendation,
            "timestamp": datetime.now().isoformat(),
            "final_decision": None
        }
        self.decisions.append(decision)
        return decision
    
    def chat(self, message: str, stream: bool = True) -> Optional[str]:
        """
        Chat with the Chief of Staff agent
        
        Args:
            message: User message
            stream: Whether to stream the response
            
        Returns:
            The agent's response or None if error
        """
        # Add system prompt if this is the first message
        if not self.conversation_history:
            self.conversation_history.append({
                "role": "system",
                "content": self.system_prompt
            })
        
        # Enhance message with context if relevant commands are detected
        enhanced_message = message
        message_lower = message.lower()
        
        # Add task context if discussing tasks
        if any(keyword in message_lower for keyword in ["task", "todo", "project"]):
            if self.tasks:
                task_summary = self._format_tasks_summary()
                enhanced_message = f"{message}\n\nCurrent tasks context:\n{task_summary}"
        
        # Add decision context if discussing decisions
        if any(keyword in message_lower for keyword in ["decision", "decide", "choose"]):
            if self.decisions:
                decision_summary = self._format_decisions_summary()
                enhanced_message = f"{message}\n\nRecent decisions context:\n{decision_summary}"
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": enhanced_message
        })
        
        try:
            payload = {
                "model": self.model,
                "messages": self.conversation_history,
                "stream": stream
            }
            
            response = requests.post(self.chat_url, json=payload, timeout=120)
            
            if response.status_code == 200:
                full_response = ""
                
                if stream:
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line)
                            if 'message' in data and 'content' in data['message']:
                                chunk = data['message']['content']
                                print(chunk, end='', flush=True)
                                full_response += chunk
                    print()
                else:
                    data = response.json()
                    full_response = data.get('message', {}).get('content', '')
                    print(full_response)
                
                # Update history with original message
                self.conversation_history[-1]["content"] = message
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": full_response
                })
                
                return full_response
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error in chat: {e}")
            return None
    
    def _format_tasks_summary(self) -> str:
        """Format tasks for context"""
        if not self.tasks:
            return "No tasks currently tracked."
        
        summary = []
        for status in ["pending", "in_progress", "completed"]:
            tasks = self.get_tasks(status)
            if tasks:
                summary.append(f"\n{status.upper()} ({len(tasks)}):")
                for task in tasks[:5]:  # Limit to 5 per status
                    summary.append(f"  - [{task['priority']}] {task['title']}")
        
        return "\n".join(summary)
    
    def _format_decisions_summary(self) -> str:
        """Format decisions for context"""
        if not self.decisions:
            return "No decisions currently tracked."
        
        summary = []
        for decision in self.decisions[-3:]:  # Last 3 decisions
            summary.append(f"\n- {decision['title']}")
            if decision['recommendation']:
                summary.append(f"  Recommendation: {decision['recommendation']}")
        
        return "\n".join(summary)
    
    def generate_summary(self) -> str:
        """Generate a summary of current state"""
        summary_parts = []
        
        # Tasks summary
        pending = len(self.get_tasks("pending"))
        in_progress = len(self.get_tasks("in_progress"))
        completed = len(self.get_tasks("completed"))
        
        summary_parts.append("📊 CURRENT STATUS SUMMARY")
        summary_parts.append("=" * 50)
        summary_parts.append(f"\nTasks: {pending} pending, {in_progress} in progress, {completed} completed")
        
        if self.notes:
            summary_parts.append(f"Notes: {len(self.notes)} recorded")
        
        if self.decisions:
            summary_parts.append(f"Decisions: {len(self.decisions)} tracked")
        
        # Recent activity
        if self.tasks:
            summary_parts.append("\n📋 RECENT TASKS:")
            for task in self.tasks[-5:]:
                status_icon = "✓" if task["status"] == "completed" else "○"
                summary_parts.append(f"  {status_icon} [{task['priority']}] {task['title']}")
        
        return "\n".join(summary_parts)
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def save_state(self, filepath: str = "chief_of_staff_state.json"):
        """Save agent state to file"""
        state = {
            "tasks": self.tasks,
            "notes": self.notes,
            "decisions": self.decisions,
            "saved_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"✓ State saved to {filepath}")
    
    def load_state(self, filepath: str = "chief_of_staff_state.json"):
        """Load agent state from file"""
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
            
            self.tasks = state.get("tasks", [])
            self.notes = state.get("notes", [])
            self.decisions = state.get("decisions", [])
            
            print(f"✓ State loaded from {filepath}")
            return True
        except FileNotFoundError:
            print(f"No saved state found at {filepath}")
            return False
        except Exception as e:
            print(f"Error loading state: {e}")
            return False


def print_help():
    """Print help information"""
    print("\n" + "=" * 70)
    print("CHIEF OF STAFF AGENT - COMMANDS")
    print("=" * 70)
    print("\nTask Management:")
    print("  add task <title> - Add a new task")
    print("  list tasks - Show all tasks")
    print("  complete <id> - Mark task as completed")
    print("  status - Show current status summary")
    print("\nNotes & Decisions:")
    print("  add note <content> - Add a note")
    print("  list notes - Show all notes")
    print("  add decision <title> - Record a decision point")
    print("\nGeneral:")
    print("  summary - Generate status summary")
    print("  save - Save current state")
    print("  load - Load saved state")
    print("  clear - Clear conversation history")
    print("  help - Show this help message")
    print("  quit/exit - End session")
    print("\nOr just chat naturally about tasks, decisions, and planning!")
    print("=" * 70 + "\n")


def main():
    """Main function to run the Chief of Staff agent"""
    print("=" * 70)
    print("🎯 CHIEF OF STAFF AGENT")
    print("Your intelligent assistant for task management and strategic support")
    print("Using model: granite3-dense:2b")
    print("=" * 70)
    print()
    
    # Initialize the agent
    agent = ChiefOfStaffAgent(model="granite3-dense:2b")
    
    # Check connection
    print("Checking Ollama connection...")
    if not agent.check_connection():
        print("❌ Error: Cannot connect to Ollama server.")
        print("Please make sure Ollama is running (ollama serve)")
        print("And that you have the granite3-dense:2b model installed.")
        print("\nTo install the model, run:")
        print("  ollama pull granite3-dense:2b")
        return
    
    print("✓ Connected to Ollama server")
    print()
    
    # Try to load previous state
    agent.load_state()
    print()
    
    print("Type 'help' for available commands or just start chatting!")
    print("=" * 70)
    print()
    
    # Interactive loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ["quit", "exit"]:
                print("\n👋 Goodbye! Stay productive!")
                break
            
            if user_input.lower() == "help":
                print_help()
                continue
            
            if user_input.lower() == "clear":
                agent.clear_history()
                print("✓ Conversation history cleared.\n")
                continue
            
            if user_input.lower() == "summary":
                print("\n" + agent.generate_summary() + "\n")
                continue
            
            if user_input.lower() == "save":
                agent.save_state()
                print()
                continue
            
            if user_input.lower() == "load":
                agent.load_state()
                print()
                continue
            
            if user_input.lower().startswith("add task "):
                title = user_input[9:].strip()
                task = agent.add_task(title)
                print(f"✓ Task added: #{task['id']} - {task['title']}\n")
                continue
            
            if user_input.lower() == "list tasks":
                tasks = agent.get_tasks()
                if not tasks:
                    print("No tasks yet.\n")
                else:
                    print("\n📋 TASKS:")
                    for task in tasks:
                        status_icon = "✓" if task["status"] == "completed" else "○"
                        print(f"  {status_icon} #{task['id']} [{task['priority']}] {task['title']} ({task['status']})")
                    print()
                continue
            
            if user_input.lower().startswith("complete "):
                try:
                    task_id = int(user_input[9:].strip())
                    task = agent.update_task_status(task_id, "completed")
                    if task:
                        print(f"✓ Task #{task_id} marked as completed!\n")
                    else:
                        print(f"✗ Task #{task_id} not found.\n")
                except ValueError:
                    print("✗ Invalid task ID.\n")
                continue
            
            if user_input.lower().startswith("add note "):
                content = user_input[9:].strip()
                note = agent.add_note(content)
                print(f"✓ Note added: #{note['id']}\n")
                continue
            
            if user_input.lower() == "list notes":
                if not agent.notes:
                    print("No notes yet.\n")
                else:
                    print("\n📝 NOTES:")
                    for note in agent.notes:
                        print(f"  #{note['id']} [{note['category']}] {note['content']}")
                    print()
                continue
            
            if user_input.lower() == "status":
                print("\n" + agent.generate_summary() + "\n")
                continue
            
            # Regular chat
            print("Agent: ", end='', flush=True)
            response = agent.chat(user_input, stream=True)
            print()
            
            if response is None:
                print("Failed to get response from the agent.\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Stay productive!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()

# Made with Bob