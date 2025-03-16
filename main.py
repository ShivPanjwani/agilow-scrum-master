#!/usr/bin/env python3
"""
Agilow Scrum Master
-------------------
An AI-powered Scrum Master assistant that maintains context across interactions
and generates Agile documentation in Notion.
"""

import sys
from utils.config_manager import ConfigManager

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
    
    # Main menu
    print("\nWhat would you like to do today?")
    print("1. Chat with Scrum Master")
    print("2. Record a meeting")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        print("\nChat functionality coming soon!")
    elif choice == "2":
        print("\nMeeting recording functionality coming soon!")
    elif choice == "3":
        print("\nGoodbye!")
        sys.exit(0)
    else:
        print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
