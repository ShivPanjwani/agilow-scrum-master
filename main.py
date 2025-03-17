#!/usr/bin/env python3
"""
Agilow Scrum Master
-------------------
An AI-powered Scrum Master assistant that maintains context across interactions
and generates Agile documentation in Notion.
"""

import sys
import os
import traceback
from datetime import datetime
import re

def main():
    try:
        print("\n" + "=" * 50)
        print("Agilow Scrum Master")
        print("=" * 50 + "\n")
        
        # Import modules here to catch import errors
        from utils.config_manager import ConfigManager
        from agents.scrum_master import get_scrum_master_response
        from api.notion_handler import append_to_notion_page
        from memory.memory_manager import MemoryManager
        
        print("✅ Modules imported successfully")
        
        # Initialize configuration
        try:
            config = ConfigManager()
            print("✅ Environment configured successfully")
        except ValueError as e:
            print(f"❌ Configuration error: {str(e)}")
            sys.exit(1)
        
        # Initialize memory manager
        memory_manager = MemoryManager()
        
        while True:
            # Main menu
            print("\nWhat would you like to do today?")
            print("1. Chat with Scrum Master")
            print("2. Record a meeting")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == "1":
                chat_with_scrum_master(config, memory_manager)
            elif choice == "2":
                print("\nMeeting recording functionality coming soon!")
            elif choice == "3":
                print("\nGoodbye!")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please try again.")
    
    except Exception as e:
        print("\n❌ An error occurred:")
        print(str(e))
        print("\nDetailed error information:")
        traceback.print_exc()
        
        # Write error to file for debugging
        with open("error_log.txt", "a") as f:
            f.write(f"\n\n--- Error at {datetime.now()} ---\n")
            f.write(str(e) + "\n")
            traceback.print_exc(file=f)
        
        print("\nError has been logged to error_log.txt")
        sys.exit(1)

def chat_with_scrum_master(config, memory_manager):
    """Chat with the Scrum Master agent"""
    from agents.scrum_master import get_scrum_master_response
    from api.notion_handler import append_to_notion_page
    
    print("\nStarting chat with Scrum Master...")
    print("(Type 'exit' to return to the main menu)")
    
    # Get context from memory manager
    context = memory_manager.get_context_string()
    
    # Track the full conversation for Notion
    conversation = []
    
    # Track meeting type
    meeting_type = None
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Only check for exact exit command
        if user_input.lower() == 'exit':
            print("\nReturning to main menu...")
            break
        
        # Add user input to conversation
        conversation.append({"role": "user", "content": user_input})
        
        # Detect meeting type if not already set
        if not meeting_type:
            if any(term in user_input.lower() for term in ["sprint planning", "plan sprint", "planning", "epics", "user stories"]):
                meeting_type = "sprint_planning"
            elif any(term in user_input.lower() for term in ["standup", "stand-up", "daily", "status update"]):
                meeting_type = "standup"
            elif any(term in user_input.lower() for term in ["retro", "retrospective", "went well", "didn't go well"]):
                meeting_type = "retrospective"
        
        try:
            # Generate response
            response = get_scrum_master_response(user_input, context)
            
            # Add response to conversation
            conversation.append({"role": "assistant", "content": response})
            
            # Display response
            print(f"\nScrum Master: {response}")
            
            # Check for save triggers in user input
            user_save_triggers = ["save to notion", "save it in notion", "save in notion", "post to notion", 
                                 "add to notion", "put in notion", "paste to notion", "save this"]
            
            # Check for save triggers in AI response
            ai_save_triggers = ["saving", "save these", "save this", "saving to notion", "save to notion", 
                               "saving into notion", "adding to notion", "append to notion"]
            
            # Check if user requested save
            if any(trigger in user_input.lower() for trigger in user_save_triggers):
                save_confirm = input("\nWould you like me to save this to Notion now? (y/n): ")
                if save_confirm.lower() in ['y', 'yes']:
                    success = save_to_notion(config, conversation, meeting_type or "general")
                    if success:
                        print("\n✅ Successfully saved to Notion!")
                        # After successful save, ask if they want to exit
                        exit_confirm = input("\nWould you like to exit the chat now? (y/n): ")
                        if exit_confirm.lower() in ['y', 'yes']:
                            print("\nReturning to main menu...")
                            break
                    else:
                        print("\n❌ Failed to save to Notion. Please try again.")
            
            # Check if AI mentioned saving
            elif any(trigger in response.lower() for trigger in ai_save_triggers):
                save_confirm = input("\nThe Scrum Master mentioned saving to Notion. Would you like to proceed? (y/n): ")
                if save_confirm.lower() in ['y', 'yes']:
                    success = save_to_notion(config, conversation, meeting_type or "general")
                    if success:
                        print("\n✅ Successfully saved to Notion!")
                        # After successful save, ask if they want to exit
                        exit_confirm = input("\nWould you like to exit the chat now? (y/n): ")
                        if exit_confirm.lower() in ['y', 'yes']:
                            print("\nReturning to main menu...")
                            break
                    else:
                        print("\n❌ Failed to save to Notion. Please try again.")
            
            # Save to memory
            memory_manager.add_exchange(user_input, response)
            
            # Update context for next iteration
            context = memory_manager.get_context_string()
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Let's continue our conversation.")
    
    print("\nReturning to main menu...")

def format_sprint_planning(content, timestamp):
    """Format sprint planning content for Notion"""
    # Extract epics and user stories using regex patterns
    epics_pattern = r"(?:Epic|📌 Sprint Epics)[^\n]*\n(.*?)(?:\n\n|\n(?:🚀|Final))"
    epics_match = re.search(epics_pattern, content, re.DOTALL)
    
    formatted = f"# Sprint Planning ({timestamp})\n\n"
    
    if epics_match:
        epics_section = epics_match.group(1)
        formatted += "## 📌 Sprint Epics\n\n"
        
        # Extract numbered/emoji epics
        epic_pattern = r"(?:\d️⃣|\d+\.|[•●]) ([^\n]+)"
        epics = re.findall(epic_pattern, epics_section)
        
        for i, epic in enumerate(epics, 1):
            formatted += f"{i}. {epic.strip()}\n"
    
    # Extract user stories
    stories_pattern = r"(?:User Story|🔹 User Story)[^\n]*\n(.*?)(?:\n\n|$)"
    stories_matches = re.findall(stories_pattern, content, re.DOTALL)
    
    if stories_matches:
        formatted += "\n## 📝 User Stories\n\n"
        
        for i, story_section in enumerate(stories_matches, 1):
            # Clean up the story text
            story_text = story_section.strip()
            formatted += f"### Story {i}\n{story_text}\n\n"
    
    # Extract final priorities if present
    priorities_pattern = r"(?:Final Sprint Prioritization|📌 Final Sprint Prioritization)[^\n]*\n(.*?)(?:\n\n|$)"
    priorities_match = re.search(priorities_pattern, content, re.DOTALL)
    
    if priorities_match:
        formatted += "\n## 🚀 Sprint Priorities\n\n"
        priorities_section = priorities_match.group(1)
        
        # Extract individual priorities
        priority_pattern = r"(?:✔|✅|\d+\.) ([^\n]+)"
        priorities = re.findall(priority_pattern, priorities_section)
        
        for i, priority in enumerate(priorities, 1):
            formatted += f"{i}. {priority.strip()}\n"
    
    return formatted

def format_standup(content, timestamp):
    """Format standup content for Notion"""
    formatted = f"# Daily Standup ({timestamp})\n\n"
    
    # Extract status sections
    done_pattern = r"(?:Done|Completed|✅ Done)[^\n]*(?:\n|:)(.*?)(?:\n\n|\n(?:In Progress|🔄|$))"
    done_match = re.search(done_pattern, content, re.DOTALL)
    
    in_progress_pattern = r"(?:In Progress|🔄 In Progress)[^\n]*(?:\n|:)(.*?)(?:\n\n|\n(?:To Do|🔜|$))"
    in_progress_match = re.search(in_progress_pattern, content, re.DOTALL)
    
    todo_pattern = r"(?:To Do|🔜 To Do|Planned)[^\n]*(?:\n|:)(.*?)(?:\n\n|$)"
    todo_match = re.search(todo_pattern, content, re.DOTALL)
    
    blockers_pattern = r"(?:Blockers|❌ Blockers|Issues)[^\n]*(?:\n|:)(.*?)(?:\n\n|$)"
    blockers_match = re.search(blockers_pattern, content, re.DOTALL)
    
    # Add Done section
    formatted += "## ✅ Done\n\n"
    if done_match:
        done_items = re.findall(r"(?:[-•✓✔]|\d+\.) ([^\n]+)", done_match.group(1))
        for item in done_items:
            formatted += f"- {item.strip()}\n"
    else:
        formatted += "- No completed items reported\n"
    
    # Add In Progress section
    formatted += "\n## 🔄 In Progress\n\n"
    if in_progress_match:
        in_progress_items = re.findall(r"(?:[-•]|\d+\.) ([^\n]+)", in_progress_match.group(1))
        for item in in_progress_items:
            formatted += f"- {item.strip()}\n"
    else:
        formatted += "- No in-progress items reported\n"
    
    # Add To Do section
    formatted += "\n## 🔜 To Do\n\n"
    if todo_match:
        todo_items = re.findall(r"(?:[-•]|\d+\.) ([^\n]+)", todo_match.group(1))
        for item in todo_items:
            formatted += f"- {item.strip()}\n"
    else:
        formatted += "- No upcoming items reported\n"
    
    # Add Blockers section if present
    if blockers_match:
        formatted += "\n## ❌ Blockers\n\n"
        blocker_items = re.findall(r"(?:[-•]|\d+\.) ([^\n]+)", blockers_match.group(1))
        for item in blocker_items:
            formatted += f"- {item.strip()}\n"
    
    return formatted

def format_retrospective(content, timestamp):
    """Format retrospective content for Notion"""
    formatted = f"# Sprint Retrospective ({timestamp})\n\n"
    
    # Extract sections
    went_well_pattern = r"(?:What Went Well|✅ What Went Well)[^\n]*(?:\n|:)(.*?)(?:\n\n|\n(?:What Didn't|What Did Not|⚠ What))"
    went_well_match = re.search(went_well_pattern, content, re.DOTALL)
    
    not_well_pattern = r"(?:What Didn't Go Well|What Did Not Go Well|⚠ What Didn't Go Well)[^\n]*(?:\n|:)(.*?)(?:\n\n|\n(?:What Changes|🔄 What Changes|Action))"
    not_well_match = re.search(not_well_pattern, content, re.DOTALL)
    
    changes_pattern = r"(?:What Changes|🔄 What Changes|Action Items)[^\n]*(?:\n|:)(.*?)(?:\n\n|$)"
    changes_match = re.search(changes_pattern, content, re.DOTALL)
    
    # Add What Went Well section
    formatted += "## ✅ What Went Well\n\n"
    if went_well_match:
        # Extract items with numbers, bullets, or emojis
        went_well_items = re.findall(r"(?:\d️⃣|\d+\.|[•●✅]|^\d+\)) ([^\n]+)", went_well_match.group(1), re.MULTILINE)
        for item in went_well_items:
            formatted += f"- {item.strip()}\n"
    else:
        formatted += "- No positive items reported\n"
    
    # Add What Didn't Go Well section
    formatted += "\n## ⚠️ What Didn't Go Well\n\n"
    if not_well_match:
        not_well_items = re.findall(r"(?:\d️⃣|\d+\.|[•●⚠]|^\d+\)) ([^\n]+)", not_well_match.group(1), re.MULTILINE)
        for item in not_well_items:
            formatted += f"- {item.strip()}\n"
    else:
        formatted += "- No improvement areas reported\n"
    
    # Add Changes section
    formatted += "\n## 🔄 What Changes We're Making\n\n"
    if changes_match:
        changes_items = re.findall(r"(?:\d️⃣|\d+\.|[•●✅📌]|^\d+\)) ([^\n]+)", changes_match.group(1), re.MULTILINE)
        for item in changes_items:
            formatted += f"- {item.strip()}\n"
    else:
        formatted += "- No action items reported\n"
    
    return formatted

def save_to_notion(config, conversation, meeting_type):
    """Save the conversation to Notion"""
    from api.notion_handler import append_to_notion_page
    
    try:
        # Get Notion credentials
        notion_api_key = config.get_notion_api_key()
        notion_page_id = config.get_notion_page_id()
        
        if not notion_api_key or not notion_page_id:
            print("❌ Notion API key or page ID not configured")
            return False
        
        # Format the conversation based on meeting type
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Find the last two assistant messages
        assistant_messages = []
        for message in conversation:
            if message["role"] == "assistant":
                assistant_messages.append(message["content"])
        
        # Get the last two messages (or just the last one if there's only one)
        if len(assistant_messages) >= 2:
            # Use the second-to-last message as it likely contains the actual content
            final_output = assistant_messages[-2]
        elif len(assistant_messages) == 1:
            final_output = assistant_messages[0]
        else:
            print("❌ No assistant output found to save")
            return False
        
        # Just add a simple header based on meeting type
        if meeting_type == "sprint_planning":
            formatted_content = f"# Sprint Planning ({timestamp})\n\n{final_output}"
        elif meeting_type == "standup":
            formatted_content = f"# Daily Standup ({timestamp})\n\n{final_output}"
        elif meeting_type == "retrospective":
            formatted_content = f"# Sprint Retrospective ({timestamp})\n\n{final_output}"
        else:
            formatted_content = f"# Meeting Notes ({timestamp})\n\n{final_output}"
        
        # Save to Notion
        print(f"Saving to Notion: {formatted_content[:100]}...")  # Print first 100 chars
        success = append_to_notion_page(notion_page_id, formatted_content)
        
        if success:
            print("\n✅ Successfully saved to Notion!")
            return True
        else:
            print("\n❌ Failed to save to Notion. Please try again.")
            return False
            
    except Exception as e:
        print(f"❌ Error saving to Notion: {str(e)}")
        traceback.print_exc()
        return False

# Update the Notion handler to debug and ensure it works
def debug_append_to_notion_page(page_id, content):
    """
    Debug version of append_to_notion_page that prints what it's doing.
    
    Args:
        page_id (str): The ID of the Notion page
        content (str): The content to append
        
    Returns:
        bool: True if successful, False otherwise
    """
    from api.notion_handler import append_to_notion_page
    
    print(f"\nAttempting to save to Notion page {page_id}")
    print(f"Content to save: {content[:100]}...")  # Print first 100 chars
    
    try:
        result = append_to_notion_page(page_id, content)
        print(f"Notion API result: {result}")
        return result
    except Exception as e:
        print(f"Notion API error: {str(e)}")
        return False

# Add this at the end of the file
if __name__ == "__main__":
    main()
    