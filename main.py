#!/usr/bin/env python3
"""
Agilow Scrum Master
-------------------
An AI-powered Scrum Master assistant that maintains context across interactions
and generates Agile documentation in Notion.
"""

import sys
import os
from datetime import datetime
from utils.config_manager import ConfigManager
from agents.scrum_master import get_scrum_master_response
from api.notion_handler import append_to_notion_page
from memory.memory_manager import MemoryManager

def chat_with_scrum_master():
    """Chat with the Scrum Master agent"""
    print("\n" + "=" * 50)
    print("Chat with Scrum Master")
    print("=" * 50)
    print("\nType 'exit' to return to the main menu.")
    
    # Initialize memory manager
    memory = MemoryManager()
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit", "back"]:
            break
        
        # Get context from memory
        context = memory.get_context_string()
        
        # Get response from Scrum Master agent
        response = get_scrum_master_response(user_input, context)
        
        # Display response
        print(f"\nScrum Master: {response}")
        
        # Add exchange to memory
        memory.add_exchange(user_input, response)
        
        # Ask if user wants to save to Notion
        save_choice = input("\nSave this to Notion? (y/n): ")
        if save_choice.lower() == "y":
            page_id = os.getenv("NOTION_PAGE_ID")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = f"## Conversation at {timestamp}\n\n**User:** {user_input}\n\n**Scrum Master:** {response}"
            
            if append_to_notion_page(page_id, content):
                print("✅ Saved to Notion!")
            else:
                print("❌ Failed to save to Notion.")

def main():
    """Main application entry point"""
    print("\n" + "=" * 50)
    print("Agilow Scrum Master")
    print("=" * 50 + "\n")
    
    # Initialize configuration
    try:
        config = ConfigManager()
        print("✅ Environment configured successfully")
    except ValueError as e:
        print(f"❌ Configuration error: {str(e)}")
        sys.exit(1)
    
    while True:
        # Main menu
        print("\nWhat would you like to do today?")
        print("1. Chat with Scrum Master")
        print("2. Record a meeting")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            chat_with_scrum_master()
        elif choice == "2":
            print("\nMeeting recording functionality coming soon!")
        elif choice == "3":
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
