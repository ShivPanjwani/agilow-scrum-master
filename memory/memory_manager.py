"""
Memory management for Agilow Scrum Master.
"""

import os
import json
from datetime import datetime

class MemoryManager:
    """Manages conversation memory for the Scrum Master agent"""
    
    def __init__(self, user_name="user"):
        """Initialize the memory manager"""
        self.user_name = user_name
        self.conversation_history = []
        self.file_path = f"data/{user_name}_memory.json"
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Load existing memory if available
        self.load_memory()
    
    def add_exchange(self, user_input, ai_response):
        """Add a conversation exchange to memory"""
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response
        }
        
        self.conversation_history.append(exchange)
        self.save_memory()
    
    def get_recent_history(self, limit=5):
        """Get recent conversation history"""
        return self.conversation_history[-limit:] if self.conversation_history else []
    
    def save_memory(self):
        """Save memory to file"""
        with open(self.file_path, "w") as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def load_memory(self):
        """Load memory from file"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    self.conversation_history = json.load(f)
        except Exception as e:
            print(f"Error loading memory: {str(e)}")
            self.conversation_history = []
    
    def get_context_string(self, limit=5):
        """Get context string for the AI"""
        recent_history = self.get_recent_history(limit)
        
        if not recent_history:
            return "No previous conversation history."
        
        context = "Recent conversation history:\n\n"
        
        for exchange in recent_history:
            timestamp = exchange.get("timestamp", "Unknown time")
            user_input = exchange.get("user_input", "")
            ai_response = exchange.get("ai_response", "")
            
            context += f"Time: {timestamp}\n"
            context += f"User: {user_input}\n"
            context += f"Scrum Master: {ai_response}\n\n"
        
        return context
