"""
Configuration management for Agilow Scrum Master.
"""

import os
from dotenv import load_dotenv

class ConfigManager:
    """Manages configuration and environment variables"""
    
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get required environment variables
        self.notion_api_key = os.getenv("NOTION_API_KEY")
        self.notion_page_id = os.getenv("NOTION_PAGE_ID")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Validate required environment variables
        self._validate_config()
        
        # Set OpenAI API key for use in other modules
        os.environ["OPENAI_API_KEY"] = self.openai_api_key
    
    def _validate_config(self):
        """Validates that all required configuration values are present"""
        missing_vars = []
        
        if not self.notion_api_key:
            missing_vars.append("NOTION_API_KEY")
        if not self.notion_page_id:
            missing_vars.append("NOTION_PAGE_ID")
        if not self.openai_api_key:
            missing_vars.append("OPENAI_API_KEY")
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. Please check your .env file.")
    
    def get_openai_api_key(self):
        """Get the OpenAI API key"""
        return self.openai_api_key
    
    def get_notion_api_key(self):
        """Get the Notion API key"""
        return self.notion_api_key
    
    def get_notion_page_id(self):
        """Get the Notion page ID"""
        return self.notion_page_id
