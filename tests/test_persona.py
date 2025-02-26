"""
Unit tests for the persona system.
"""

import sys
import os
# Add the parent directory to path so Python can find the mode_0 package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from unittest.mock import MagicMock, patch

class TestPersonaSystem(unittest.TestCase):
    """Test cases for persona system"""
    
    def setUp(self):
        # Mock database manager
        self.mock_db = MagicMock()
        self.mock_db.get_user_profile = MagicMock(return_value={})
        self.mock_db.update_user_profile = MagicMock()
        
        # Mock responses
        self.test_responses = {
            "greetings": ["Hey there, {username}!"],
            "generic_responses": ["That's interesting, {username}!"],
            "conversation_starters": ["Test starter"],
        }
        
        # Create patch for open to return mock response data
        self.open_patch = patch("builtins.open", unittest.mock.mock_open(
            read_data=json.dumps(self.test_responses)
        ))
    
    def test_greeting_generation(self):
        """Test greeting generation"""
        with self.open_patch:
            from mode_0.persona.persona_system import PersonaSystem
            persona = PersonaSystem(self.mock_db)
            
            # Override responses directly
            persona.responses = self.test_responses
            
            # Test greeting
            greeting = asyncio.run(persona.generate_greeting("testuser", "user123"))
            self.assertEqual(greeting, "Hey there, testuser!")
    
    def test_response_generation(self):
        """Test response generation"""
        with self.open_patch:
            from mode_0.persona.persona_system import PersonaSystem
            persona = PersonaSystem(self.mock_db)
            
            # Override responses directly
            persona.responses = self.test_responses
            
            # Create mock message
            mock_message = MagicMock()
            mock_message.content = "Hello bot"
            mock_message.author = MagicMock()
            mock_message.author.display_name = "testuser"
            
            # Test response
            response = asyncio.run(persona.generate_response(mock_message))
            self.assertEqual(response, "That's interesting, testuser!")

# More test cases would be added here
