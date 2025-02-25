"""
Persona system for the Mode_0 bot.
"""
import json
import random
import logging
from datetime import datetime, timedelta

logger = logging.getLogger("mode_0.persona")

class PersonaSystem:
    """Manages bot personality and responses"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        logger.info("Initializing persona system")
        
        # Load persona configuration
        try:
            with open("mode_0/config/persona_config.json", "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            logger.warning("Persona config not found, using defaults")
            self.config = self._default_persona_config()
        
        # Load response templates
        try:
            with open("mode_0/config/responses.json", "r") as f:
                self.responses = json.load(f)
        except FileNotFoundError:
            logger.warning("Response templates not found, using defaults")
            self.responses = self._default_responses()
        
        # Persona state
        self.mood = "neutral"  # neutral, happy, excited, calm, etc.
        self.conversation_topics = {}
        self.learning_rate = 0.05  # How quickly persona adapts
    
    def _default_persona_config(self):
        """Default persona configuration"""
        return {
            "base_personality": {
                "friendly": 0.8,
                "humor": 0.7,
                "helpfulness": 0.9,
                "edginess": 0.5
            },
            "learning_rate": 0.05,
            "response_timing": {
                "min_delay": 1,
                "max_delay": 3
            }
        }
    
    def _default_responses(self):
        """Default response templates"""
        return {
            "greetings": [
                "Hey there, {username}!",
                "What's up, {username}!",
                "Hello, {username}!"
            ],
            "generic_responses": [
                "That's interesting, {username}!",
                "I hear you, {username}.",
                "Nice one, {username}!"
            ],
            "question_responses": [
                "Good question, {username}! Let me think...",
                "Hmm, that's a tough one, {username}.",
                "Let me see if I can help with that, {username}."
            ],
            "conversation_starters": [
                "Anyone excited for the weekend?",
                "What's everyone listening to lately?",
                "How's the chat doing today?"
            ]
        }
    
    async def generate_greeting(self, username, user_id):
        """Generate personalized greeting based on user history"""
        # Implementation to be added
        return random.choice(self.responses["greetings"]).format(username=username)
    
    async def parse_and_update_profile(self, message, user_id):
        """Extract information from message to update user profile"""
        # Implementation to be added
        pass
    
    async def get_conversation_starter(self, channel_mood=None):
        """Generate a conversation starter based on channel mood"""
        # Implementation to be added
        return random.choice(self.responses["conversation_starters"])
    
    async def generate_response(self, message, is_mentioned=False):
        """Generate response based on message content and context"""
        # Implementation to be added
        username = message.author.display_name
        return random.choice(self.responses["generic_responses"]).format(username=username)
    
    def get_current_mode(self):
        """Get current bot personality mode"""
        return self.mood
