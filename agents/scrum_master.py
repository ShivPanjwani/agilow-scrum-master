"""
Scrum Master agent for Agilow Scrum Master.
"""

import os
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
    You are an expert Agile Scrum Master assistant.
    
    Your role is to help the team with:
    1. Sprint planning
    2. Daily standups
    3. Sprint reviews
    4. Sprint retrospectives
    5. Backlog refinement
    
    Provide helpful, concise responses based on Agile best practices.
    Format your responses appropriately based on the type of meeting or request.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
    ]
    
    if context:
        messages.append({"role": "system", "content": f"Context: {context}"})
        
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    
    return response.choices[0].message.content
