"""
Scrum Master agent for Agilow Scrum Master.
"""

import os
import time
import sys
from openai import OpenAI

def get_scrum_master_response(user_input, context=""):
    """
    Gets a response from the Scrum Master agent.
    
    Args:
        user_input (str): The user's input
        context (str): Additional context for the agent
        
    Returns:
        str: The agent's response
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system_prompt = """
    You are an expert Agile Scrum Master assistant with Notion integration capabilities.
    
    Your role is to help the team with:
    1. Sprint planning
    2. Daily standups
    3. Sprint reviews
    4. Sprint retrospectives
    5. Backlog refinement
    
    You have the ability to save conversations, epics, user stories, and other Agile artifacts directly to Notion.
    When users mention wanting to add items to Notion or their backlog, acknowledge that you can help with this
    and that the information will be automatically saved to their Notion workspace.
    
    Provide helpful, concise responses based on Agile best practices.
    Format your responses appropriately based on the type of meeting or request.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
    ]
    
    if context:
        messages.append({"role": "system", "content": f"Context: {context}"})
        
    messages.append({"role": "user", "content": user_input})
    
    # Show a loading indicator
    print("\nThinking", end="")
    sys.stdout.flush()
    
    try:
        # Make the API call with a timeout
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            timeout=60  # 60 second timeout
        )
        print("\r" + " " * 20 + "\r", end="")  # Clear the loading indicator
        return response.choices[0].message.content
    except Exception as e:
        print("\r" + " " * 20 + "\r", end="")  # Clear the loading indicator
        print(f"\n❌ Error getting response: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request. Please try again with a shorter message."