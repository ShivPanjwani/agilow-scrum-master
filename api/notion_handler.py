"""
Notion API integration for Agilow Scrum Master.
"""

import os
import requests
from datetime import datetime

def append_to_notion_page(page_id, content):
    """
    Appends content to a Notion page.
    
    Args:
        page_id (str): The ID of the Notion page
        content (str): The content to append
        
    Returns:
        bool: True if successful, False otherwise
    """
    notion_api_key = os.getenv("NOTION_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    # Convert content to Notion blocks
    blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }
                ]
            }
        }
    ]
    
    data = {"children": blocks}
    response = requests.patch(url, headers=headers, json=data)
    
    return response.status_code >= 200 and response.status_code < 300

def get_notion_page_content(page_id):
    """
    Gets the content of a Notion page.
    
    Args:
        page_id (str): The ID of the Notion page
        
    Returns:
        str: The content of the page
    """
    notion_api_key = os.getenv("NOTION_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2022-06-28"
    }
    
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    else:
        print(f"Error getting Notion page content: {response.status_code}")
        return None
