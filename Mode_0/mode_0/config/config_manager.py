"""
Configuration management for the Mode_0 bot.
"""
import json
import os
import logging
from pathlib import Path

logger = logging.getLogger("mode_0.config")

class ConfigManager:
    """Manages bot configuration"""
    
    def __init__(self, config_path="mode_0/config/config.json"):
        self.config_path = config_path
        self.config = {}
        
        # Load configuration
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
        except FileNotFoundError:
            logger.warning(f"Configuration file not found at {self.config_path}")
            # Check for template
            template_path = Path(self.config_path).parent / "config.template.json"
            if template_path.exists():
                logger.info(f"Template exists at {template_path}. Please copy to {self.config_path} and configure.")
            self.config = {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in configuration file: {self.config_path}")
            self.config = {}
    
    def get(self, key, default=None):
        """Get configuration value by dot-notation key"""
        if not self.config:
            return default
            
        # Handle dot notation (e.g., "twitch.oauth_token")
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
    
    def set(self, key, value):
        """Set configuration value by dot-notation key"""
        keys = key.split(".")
        
        # Navigate to the correct nested dictionary
        current = self.config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        
        logger.info(f"Configuration saved to {self.config_path}")
