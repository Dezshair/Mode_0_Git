#!/usr/bin/env python3
"""
Mode_0 Twitch Bot - Project Structure Setup Script
This script creates the complete file structure for the Mode_0 Twitch bot project.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import json


# Configuration
PROJECT_NAME = "mode_0"
DIRECTORIES = [
    # Core structure
    "",
    "mode_0",
    "mode_0/core",
    "mode_0/persona",
    "mode_0/streamelements",
    "mode_0/database",
    "mode_0/utils",
    "mode_0/config",
    # Support directories
    "scripts",
    "tests",
    "docs",
    # Runtime directories
    "logs",
    "data",
]

FILES = [
    # Root project files
    {"path": "README.md", "content": """# Mode_0 Twitch Bot

A custom Twitch bot for DJ Qwazi905 with StreamElements integration, intelligent chat engagement, and persona-based interactions.

## Features

- Twitch chat integration
- StreamElements command & loyalty integration
- User memory and profiling
- Autonomous chat engagement
- Customizable bot persona

## Setup

1. Create and activate virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - Copy `config/config.template.json` to `config/config.json`
   - Edit with your credentials and settings

4. Run the bot:
   ```
   python -m mode_0
   ```
"""},
    
    {"path": "requirements.txt", "content": """# Core dependencies
twitchio>=2.6.0
aiohttp>=3.8.4
sqlalchemy>=2.0.0
apscheduler>=3.10.1

# StreamElements integration
websockets>=11.0.3

# NLP/Persona
spacy>=3.6.0

# Utilities
python-dotenv>=1.0.0
colorlog>=6.7.0
"""},
    
    {"path": ".gitignore", "content": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
*.egg-info/
.installed.cfg
*.egg

# Project specific
config/config.json
config/credentials.json
logs/
data/*.db
data/user_profiles/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS specific
.DS_Store
Thumbs.db
"""},

    # Main package
    {"path": "mode_0/__init__.py", "content": """\"\"\"
Mode_0 - Custom Twitch Bot for DJ Qwazi905
\"\"\"

__version__ = '0.1.0'
"""},
    
    {"path": "mode_0/__main__.py", "content": """\"\"\"
Entry point for running the Mode_0 bot.
\"\"\"
from mode_0.core.bot import Mode0Bot

def main():
    \"\"\"Initialize and run the bot\"\"\"
    bot = Mode0Bot()
    bot.run()

if __name__ == "__main__":
    main()
"""},
    
    # Core bot modules
    {"path": "mode_0/core/__init__.py", "content": ""},
    
    {"path": "mode_0/core/bot.py", "content": """\"\"\"
Core bot implementation for Mode_0.
\"\"\"
import asyncio
import logging
from twitchio.ext import commands
from mode_0.config.config_manager import ConfigManager
from mode_0.database.db_manager import DatabaseManager
from mode_0.persona.persona_system import PersonaSystem
from mode_0.streamelements.se_manager import StreamElementsManager
from mode_0.utils.logger import setup_logger

logger = logging.getLogger("mode_0.core.bot")

class Mode0Bot(commands.Bot):
    \"\"\"Main bot class for Mode_0\"\"\"
    
    def __init__(self):
        # Set up logging
        setup_logger()
        logger.info("Initializing Mode_0 bot")
        
        # Load configuration
        self.config = ConfigManager()
        
        # Initialize bot with Twitch credentials
        super().__init__(
            token=self.config.get("twitch.oauth_token"),
            prefix=self.config.get("bot.command_prefix", "!"),
            initial_channels=[self.config.get("twitch.channel")]
        )
        
        # Set up database
        self.db = DatabaseManager(self.config.get("database.path", "data/mode_0.db"))
        
        # Initialize persona system
        self.persona = PersonaSystem(self.db)
        
        # Initialize StreamElements manager
        self.se_manager = StreamElementsManager(
            jwt_token=self.config.get("streamelements.jwt"),
            channel_id=self.config.get("streamelements.channel_id")
        )
        
        # Bot state
        self.message_queue = asyncio.Queue()
        self.active_chatters = {}
        
        # Register command cogs
        self._register_commands()
        
        # Start processing tasks
        self.loop.create_task(self._process_message_queue())
        self.loop.create_task(self._idle_chat_initiator())
    
    def _register_commands(self):
        \"\"\"Register command modules\"\"\"
        # To be implemented - register command cogs here
        pass
    
    async def event_ready(self):
        \"\"\"Called once when bot connects to Twitch\"\"\"
        logger.info(f"Bot connected to Twitch | {self.nick}")
        logger.info(f"Connected to channels: {', '.join(self.initial_channels)}")
        
        # Connect to StreamElements
        await self.se_manager.connect()
    
    async def event_message(self, message):
        \"\"\"Event handler for incoming messages\"\"\"
        # Ignore messages from the bot itself
        if message.author is not None and message.author.name.lower() == self.nick.lower():
            return
            
        # Process commands if message starts with prefix
        await self.handle_commands(message)
        
        # Queue message for processing
        if message.author is not None:
            await self.message_queue.put(message)
    
    async def _process_message_queue(self):
        \"\"\"Process messages from the queue\"\"\"
        while True:
            message = await self.message_queue.get()
            try:
                # Implementation to be added
                pass
            except Exception as e:
                logger.error(f"Error processing message: {e}")
            finally:
                self.message_queue.task_done()
    
    async def _idle_chat_initiator(self):
        \"\"\"Initiate conversation when chat is quiet\"\"\"
        # Implementation to be added
        pass
"""},
    
    {"path": "mode_0/core/commands.py", "content": """\"\"\"
Command handlers for Mode_0 bot.
\"\"\"
from twitchio.ext import commands
import logging

logger = logging.getLogger("mode_0.core.commands")

class BasicCommands(commands.Cog):
    \"\"\"Basic bot commands\"\"\"
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="help")
    async def help_command(self, ctx):
        \"\"\"Display help information\"\"\"
        await ctx.send(f"@{ctx.author.name} Available commands: !help, !about, !socials")
    
    @commands.command(name="about")
    async def about_command(self, ctx):
        \"\"\"Display information about the bot\"\"\"
        await ctx.send(f"@{ctx.author.name} I'm Mode_0, a custom bot for DJ Qwazi905's channel!")
    
    @commands.command(name="socials")
    async def socials_command(self, ctx):
        \"\"\"Display DJ Qwazi905's social media links\"\"\"
        await ctx.send(f"@{ctx.author.name} Follow DJ Qwazi905 on: Twitch: twitch.tv/Qwazi905 | Twitter: x.com/Qwazi905 | SoundCloud: soundcloud.com/qwaziqwazi905")

class AdminCommands(commands.Cog):
    \"\"\"Admin-only commands\"\"\"
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="botmode")
    async def mode_command(self, ctx, mode=None):
        \"\"\"Change bot behavior mode (admin only)\"\"\"
        # Check if user is admin
        if not await self._is_admin(ctx.author.id):
            return
        
        if mode is None:
            await ctx.send(f"@{ctx.author.name} Current bot mode: {self.bot.persona.get_current_mode()}")
            return
        
        # Set mode
        # Implementation to be added
        await ctx.send(f"@{ctx.author.name} Bot mode changed to: {mode}")
    
    async def _is_admin(self, user_id):
        \"\"\"Check if user is an admin\"\"\"
        # Implementation to be added
        return False
"""},
    
    # Persona system
    {"path": "mode_0/persona/__init__.py", "content": ""},
    
    {"path": "mode_0/persona/persona_system.py", "content": """\"\"\"
Persona system for the Mode_0 bot.
\"\"\"
import json
import random
import logging
from datetime import datetime, timedelta

logger = logging.getLogger("mode_0.persona")

class PersonaSystem:
    \"\"\"Manages bot personality and responses\"\"\"
    
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
        \"\"\"Default persona configuration\"\"\"
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
        \"\"\"Default response templates\"\"\"
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
        \"\"\"Generate personalized greeting based on user history\"\"\"
        # Implementation to be added
        return random.choice(self.responses["greetings"]).format(username=username)
    
    async def parse_and_update_profile(self, message, user_id):
        \"\"\"Extract information from message to update user profile\"\"\"
        # Implementation to be added
        pass
    
    async def get_conversation_starter(self, channel_mood=None):
        \"\"\"Generate a conversation starter based on channel mood\"\"\"
        # Implementation to be added
        return random.choice(self.responses["conversation_starters"])
    
    async def generate_response(self, message, is_mentioned=False):
        \"\"\"Generate response based on message content and context\"\"\"
        # Implementation to be added
        username = message.author.display_name
        return random.choice(self.responses["generic_responses"]).format(username=username)
    
    def get_current_mode(self):
        \"\"\"Get current bot personality mode\"\"\"
        return self.mood
"""},
    
    {"path": "mode_0/persona/user_profiler.py", "content": """\"\"\"
User profiling system for the Mode_0 bot.
\"\"\"
import json
import logging
from datetime import datetime

logger = logging.getLogger("mode_0.persona.profiler")

class UserProfiler:
    \"\"\"Analyzes and builds user profiles\"\"\"
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    async def get_user_profile(self, user_id):
        \"\"\"Get user profile data\"\"\"
        return await self.db.get_user_profile(user_id)
    
    async def update_profile(self, user_id, message):
        \"\"\"Update user profile based on message content\"\"\"
        profile = await self.get_user_profile(user_id)
        
        # Initialize profile if empty
        if not profile:
            profile = {
                "first_seen": datetime.now().isoformat(),
                "visits": 1,
                "interests": [],
                "conversations": []
            }
        
        # Update profile data
        profile["last_seen"] = datetime.now().isoformat()
        profile["visits"] = profile.get("visits", 0) + 1
        
        # Extract potential topics of interest
        # Implementation to be added
        
        # Update profile in database
        await self.db.update_user_profile(user_id, profile)
        return profile
    
    async def analyze_message(self, message):
        \"\"\"Analyze message content for insights\"\"\"
        # Implementation to be added
        return {}
"""},
    
    # StreamElements integration
    {"path": "mode_0/streamelements/__init__.py", "content": ""},
    
    {"path": "mode_0/streamelements/se_manager.py", "content": """\"\"\"
StreamElements integration for the Mode_0 bot.
\"\"\"
import aiohttp
import asyncio
import json
import logging
import random
import websockets

logger = logging.getLogger("mode_0.streamelements")

class StreamElementsManager:
    \"\"\"Handles all interactions with StreamElements API\"\"\"
    
    def __init__(self, jwt_token, channel_id):
        self.jwt_token = jwt_token
        self.channel_id = channel_id
        self.headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
        self.base_url = "https://api.streamelements.com/kappa/v2"
        self.ws_url = "wss://realtime.streamelements.com/socket.io"
        self.ws = None
        self.connected = False
        self.commands = {}
        self.games = {
            "solo": [],
            "group": [],
            "duel": []
        }
        
        logger.info("StreamElements manager initialized")
    
    async def connect(self):
        \"\"\"Connect to StreamElements API and WebSocket\"\"\"
        # Fetch available commands and games
        await self.fetch_commands()
        await self.fetch_games()
        
        # Connect to WebSocket for real-time events
        await self.connect_websocket()
    
    async def fetch_commands(self):
        \"\"\"Fetch available commands from StreamElements\"\"\"
        # Implementation to be added
        pass
    
    async def fetch_games(self):
        \"\"\"Categorize commands into game types\"\"\"
        # Implementation to be added
        pass
    
    async def connect_websocket(self):
        \"\"\"Connect to StreamElements WebSocket\"\"\"
        # Implementation to be added
        pass
    
    async def execute_command(self, channel, command, *args):
        \"\"\"Execute a StreamElements command in the channel\"\"\"
        # Implementation to be added
        pass
    
    async def play_solo_game(self, channel):
        \"\"\"Select and play a random solo game\"\"\"
        # Implementation to be added
        pass
    
    async def play_group_game(self, channel):
        \"\"\"Select and play a random group game\"\"\"
        # Implementation to be added
        pass
    
    async def play_duel_game(self, channel, opponent):
        \"\"\"Start a duel game with an opponent\"\"\"
        # Implementation to be added
        pass
"""},
    
    {"path": "mode_0/streamelements/se_events.py", "content": """\"\"\"
StreamElements event handlers.
\"\"\"
import json
import logging
import asyncio

logger = logging.getLogger("mode_0.streamelements.events")

class StreamElementsEvents:
    \"\"\"Handles StreamElements events from WebSocket\"\"\"
    
    def __init__(self, bot):
        self.bot = bot
    
    async def handle_event(self, event_data):
        \"\"\"Process StreamElements event\"\"\"
        event_type = event_data.get("type")
        
        if event_type == "follower-latest":
            await self.handle_follow(event_data)
        elif event_type == "subscriber-latest":
            await self.handle_subscription(event_data)
        elif event_type == "tip-latest":
            await self.handle_tip(event_data)
        elif event_type == "host-latest":
            await self.handle_host(event_data)
        elif event_type == "raid-latest":
            await self.handle_raid(event_data)
        elif event_type == "redemption-latest":
            await self.handle_redemption(event_data)
    
    async def handle_follow(self, data):
        \"\"\"Handle new follower\"\"\"
        # Implementation to be added
        pass
    
    async def handle_subscription(self, data):
        \"\"\"Handle new subscription\"\"\"
        # Implementation to be added
        pass
    
    async def handle_tip(self, data):
        \"\"\"Handle new tip/donation\"\"\"
        # Implementation to be added
        pass
    
    async def handle_host(self, data):
        \"\"\"Handle channel host\"\"\"
        # Implementation to be added
        pass
    
    async def handle_raid(self, data):
        \"\"\"Handle channel raid\"\"\"
        # Implementation to be added
        pass
    
    async def handle_redemption(self, data):
        \"\"\"Handle point redemption\"\"\"
        # Implementation to be added
        pass
"""},
    
    # Database
    {"path": "mode_0/database/__init__.py", "content": ""},
    
    {"path": "mode_0/database/db_manager.py", "content": """\"\"\"
Database management for the Mode_0 bot.
\"\"\"
import sqlite3
import json
import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("mode_0.database")

class DatabaseManager:
    \"\"\"Handles all database operations\"\"\"
    
    def __init__(self, db_path):
        self.db_path = db_path
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Create tables
        self.setup_database()
        logger.info(f"Database initialized at {db_path}")
    
    def setup_database(self):
        \"\"\"Create database tables if they don't exist\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            display_name TEXT,
            first_seen TIMESTAMP,
            last_seen TIMESTAMP,
            message_count INTEGER DEFAULT 0,
            profile TEXT
        )
        ''')
        
        # Create messages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            content TEXT,
            channel TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        # Create conversations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            user_id TEXT,
            summary TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    async def add_or_update_user(self, user_id, username, display_name):
        \"\"\"Add new user or update existing user\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        now = datetime.now()
        
        if user:
            # Update existing user
            cursor.execute('''
            UPDATE users 
            SET username = ?, display_name = ?, last_seen = ?, message_count = message_count + 1
            WHERE user_id = ?
            ''', (username, display_name, now, user_id))
        else:
            # Add new user
            cursor.execute('''
            INSERT INTO users (user_id, username, display_name, first_seen, last_seen, message_count, profile)
            VALUES (?, ?, ?, ?, ?, 1, '{}')
            ''', (user_id, username, display_name, now, now))
        
        conn.commit()
        conn.close()
    
    async def add_message(self, user_id, content, channel):
        \"\"\"Store message in database\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO messages (user_id, content, channel, timestamp)
        VALUES (?, ?, ?, ?)
        ''', (user_id, content, channel, datetime.now()))
        
        conn.commit()
        conn.close()
    
    async def get_user_profile(self, user_id):
        \"\"\"Get user profile data\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT profile FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return json.loads(result[0])
        return {}
    
    async def update_user_profile(self, user_id, profile_data):
        \"\"\"Update user profile\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE users 
        SET profile = ?
        WHERE user_id = ?
        ''', (json.dumps(profile_data), user_id))
        
        conn.commit()
        conn.close()
"""},
    
    {"path": "mode_0/database/models.py", "content": """\"\"\"
Database models for the Mode_0 bot.
\"\"\"
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any

@dataclass
class User:
    \"\"\"User model\"\"\"
    user_id: str
    username: str
    display_name: str
    first_seen: datetime
    last_seen: datetime
    message_count: int
    profile: Dict[str, Any]

@dataclass
class Message:
    \"\"\"Message model\"\"\"
    id: Optional[int]
    user_id: str
    content: str
    channel: str
    timestamp: datetime

@dataclass
class Conversation:
    \"\"\"Conversation model\"\"\"
    id: Optional[int]
    start_time: datetime
    end_time: Optional[datetime]
    user_id: str
    summary: Optional[str]
    messages: List[Message] = None
"""},
    
    # Utils
    {"path": "mode_0/utils/__init__.py", "content": ""},
    
    {"path": "mode_0/utils/logger.py", "content": """\"\"\"
Logging configuration for the Mode_0 bot.
\"\"\"
import logging
import os
import sys
from datetime import datetime
import colorlog

def setup_logger(level=logging.INFO):
    \"\"\"Set up logging configuration\"\"\"
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("mode_0")
    logger.setLevel(level)
    
    # Don't propagate to root logger
    logger.propagate = False
    
    # Clear existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Create console handler with color formatting
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(level)
    console_format = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_format)
    
    # Create file handler
    today = datetime.now().strftime("%Y-%m-%d")
    file_handler = logging.FileHandler(f"logs/mode_0_{today}.log")
    file_handler.setLevel(level)
    file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_format)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
"""},
    
    {"path": "mode_0/utils/helpers.py", "content": """\"\"\"
Helper functions for the Mode_0 bot.
\"\"\"
import random
import time
from datetime import datetime, timedelta

def get_random_delay(min_seconds=1, max_seconds=3):
    \"\"\"Get random delay for human-like response timing\"\"\"
    return random.uniform(min_seconds, max_seconds)

def format_duration(seconds):
    \"\"\"Format seconds into human-readable duration\"\"\"
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''}"
    else:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''}"

def calculate_time_since(timestamp):
    \"\"\"Calculate human-readable time since timestamp\"\"\"
    if isinstance(timestamp, str):
        dt = datetime.fromisoformat(timestamp)
    else:
        dt = timestamp
    
    now = datetime.now()
    diff = now - dt
    
    if diff < timedelta(minutes=1):
        return "just now"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff < timedelta(days=7):
        days = diff.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif diff < timedelta(days=30):
        weeks = int(diff.days / 7)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        months = int(diff.days / 30)
        return f"{months} month{'s' if months != 1 else ''} ago"
"""},
    
    # Config
    {"path": "mode_0/config/__init__.py", "content": ""},
    
    {"path": "mode_0/config/config_manager.py", "content": """\"\"\"
Configuration management for the Mode_0 bot.
\"\"\"
import json
import os
import logging
from pathlib import Path

logger = logging.getLogger("mode_0.config")

class ConfigManager:
    \"\"\"Manages bot configuration\"\"\"
    
    def __init__(self, config_path="mode_0/config/config.json"):
        self.config_path = config_path
        self.config = {}
        
        # Load configuration
        self.load_config()
    
    def load_config(self):
        \"\"\"Load configuration from file\"\"\"
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
        \"\"\"Get configuration value by dot-notation key\"\"\"
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
        \"\"\"Set configuration value by dot-notation key\"\"\"
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
        \"\"\"Save configuration to file\"\"\"
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        
        logger.info(f"Configuration saved to {self.config_path}")
"""},
    
    {"path": "mode_0/config/config.template.json", "content": """{
    "twitch": {
        "oauth_token": "YOUR_OAUTH_TOKEN",
        "channel": "YOUR_CHANNEL_NAME"
    },
    "streamelements": {
        "jwt": "YOUR_STREAMELEMENTS_JWT",
        "channel_id": "YOUR_STREAMELEMENTS_CHANNEL_ID"
    },
    "bot": {
        "name": "Mode_0",
        "command_prefix": "!",
        "auto_engage": true,
        "engagement_interval": 600,
        "admin_users": ["YOUR_USER_ID"]
    },
    "database": {
        "path": "data/mode_0.db"
    },
    "logging": {
        "level": "INFO"
    }
}"""},
    
    {"path": "mode_0/config/responses.json", "content": """{
    "greetings": [
        "Hey there, {username}!",
        "What's up, {username}!",
        "Hello, {username}!",
        "Yo {username}! Welcome to the stream!"
    ],
    "first_time_greetings": [
        "Welcome, {username}! First time here? Great to meet you!",
        "Hey {username}! Nice to see a new face in the chat!",
        "What's up {username}! Welcome to DJ Qwazi905's stream!"
    ],
    "quick_return_greetings": [
        "Back so soon, {username}? Can't get enough, huh?",
        "There you are again, {username}! Missed us?",
        "Welcome back, {username}! That was quick!"
    ],
    "same_day_greetings": [
        "Welcome back, {username}! Glad you could join us again today!",
        "Hey {username}! Thanks for coming back!",
        "Look who's back for more! Hi {username}!"
    ],
    "week_greetings": [
        "Hey {username}! Good to see you this week!",
        "Welcome back, {username}! Been a few days!",
        "{username} has returned! How's your week been?"
    ],
    "long_absence_greetings": [
        "Whoa, {username} is back! It's been a while!",
        "Look who it is! {username} has returned!",
        "The legend returns! Welcome back, {username}!"
    ],
    "generic_responses": [
        "That's interesting, {username}!",
        "I hear you, {username}.",
        "Nice one, {username}!",
        "Totally agree with you, {username}!",
        "Thanks for sharing that, {username}!"
    ],
    "question_responses": [
        "Good question, {username}! Let me think...",
        "Hmm, that's a tough one, {username}.",
        "Let me see if I can help with that, {username}.",
        "That's a great question, {username}!"
    ],
    "mention_responses": [
        "You called, {username}?",
        "I'm here, {username}!",
        "What's up, {username}?",
        "How can I help, {username}?"
    ],
    "gratitude_responses": [
        "You're welcome!",
        "Anytime!",
        "Happy to help!",
        "No problem at all!"
    ],
    "status_responses": [
        "I'm doing great! Just vibing to these beats!",
        "All systems operational and ready to party!",
        "Feeling energetic and ready for the stream!",
        "I'm fantastic! How could I not be with this music?"
    ],
    "conversation_starters": [
        "Anyone excited for the weekend?",
        "What's everyone listening to lately?",
        "How's the chat doing today?",
        "If you could only listen to one music genre forever, what would it be?",
        "What's the best concert you've ever been to?",
        "Anyone catch any good streams lately?",
        "Hot take: pineapple DOES belong on pizza. Discuss.",
        "What's your favorite track that DJ Qwazi905 plays?"
    ],
    "quiet_starters": [
        "It's quiet in here... too quiet. Let's change that!",
        "Perfect time for a chat! What's on everyone's mind?",
        "While it's chill, what music should DJ Qwazi905 play next stream?",
        "Let's get some energy in here! How's everyone doing?"
    ],
    "active_starters": [
        "The chat is popping off! Let's keep the energy going!",
        "Loving the vibes in chat today!",
        "You all are on fire today! What's got everyone so energetic?",
        "This is exactly the energy we need! What track is hitting right now?"
    ],
    "gaming_starters": [
        "Who's ready for some chat games?",
        "Let's play something together in chat!",
        "I'm feeling lucky today. Anyone up for a game?",
        "Time to test your luck with some StreamElements games!"
    ],
    "help_message": "I'm Mode_0, DJ Qwazi905's chat bot! Try commands like !help, !about, !socials, or just chat with me!"
}"""},
    
    {"path": "mode_0/config/persona_config.json", "content": """{
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
    },
    "engagement": {
        "mention_response_rate": 1.0,
        "direct_question_rate": 0.9,
        "general_chat_rate": 0.3,
        "idle_chat_interval": {
            "min_minutes": 5,
            "max_minutes": 15
        }
    },
    "topics": {
        "preferred": [
            "music",
            "dj",
            "hard house",
            "electronic",
            "streaming",
            "events"
        ],
        "engagement_boost": [
            "qwazi905",
            "hard house",
            "dj",
            "new release"
        ]
    }
}"""},
    
    # Scripts
    {"path": "scripts/install.py", "content": """#!/usr/bin/env python3
\"\"\"
Installation script for Mode_0 Twitch Bot.
\"\"\"
import os
import sys
import subprocess
import platform
import getpass

def check_python_version():
    \"\"\"Check Python version is 3.11+\"\"\"
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("Error: Python 3.11 or higher is required")
        sys.exit(1)
    print(f"Python version OK: {sys.version}")

def setup_venv():
    \"\"\"Set up virtual environment\"\"\"
    print("Setting up virtual environment...")
    
    # Check if venv exists
    if os.path.exists("venv"):
        response = input("Virtual environment already exists. Recreate? (y/n): ")
        if response.lower() != 'y':
            print("Using existing virtual environment")
            return
        
        # Remove existing venv
        if platform.system() == "Windows":
            os.system("rmdir /s /q venv")
        else:
            os.system("rm -rf venv")
    
    # Create new venv
    subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    print("Virtual environment created")

def install_dependencies():
    \"\"\"Install required packages\"\"\"
    print("Installing Python dependencies...")
    
    # Get path to pip in virtual environment
    if platform.system() == "Windows":
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
    
    # Upgrade pip
    subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
    
    # Install from requirements.txt
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
    
    print("Dependencies installed successfully")

def setup_config():
    \"\"\"Set up configuration file\"\"\"
    config_path = "mode_0/config/config.json"
    template_path = "mode_0/config/config.template.json"
    
    # Check if config already exists
    if os.path.exists(config_path):
        response = input("Configuration file already exists. Recreate? (y/n): ")
        if response.lower() != 'y':
            print("Using existing configuration")
            return
    
    # Copy template to config
    with open(template_path, 'r') as template_file:
        template = template_file.read()
    
    # Get Twitch OAuth token
    print("\\nTwitch OAuth Token")
    print("You can get a token from https://twitchtokengenerator.com/")
    oauth_token = getpass.getpass("Enter Twitch OAuth token: ")
    template = template.replace("YOUR_OAUTH_TOKEN", oauth_token)
    
    # Get channel name
    channel = input("Enter channel name (without @): ")
    template = template.replace("YOUR_CHANNEL_NAME", channel)
    
    # Get StreamElements JWT
    print("\\nStreamElements JWT Token")
    print("You can get this from StreamElements dashboard > Bot > Show Secrets")
    se_jwt = getpass.getpass("Enter StreamElements JWT: ")
    template = template.replace("YOUR_STREAMELEMENTS_JWT", se_jwt)
    
    # Get StreamElements channel ID
    print("\\nStreamElements Channel ID")
    print("This is found in the URL when you're on the StreamElements dashboard")
    se_channel_id = input("Enter StreamElements channel ID: ")
    template = template.replace("YOUR_STREAMELEMENTS_CHANNEL_ID", se_channel_id)
    
    # Get admin user ID
    admin_id = input("Enter your Twitch user ID for admin access: ")
    template = template.replace("YOUR_USER_ID", admin_id)
    
    # Write config file
    with open(config_path, 'w') as config_file:
        config_file.write(template)
    
    print(f"Configuration saved to {config_path}")

def setup_service():
    \"\"\"Set up system service for bot\"\"\"
    if platform.system() == "Windows":
        setup_windows_service()
    else:
        setup_linux_service()

def setup_windows_service():
    \"\"\"Set up Windows service\"\"\"
    print("Setting up Windows service...")
    
    # Create batch file
    with open("run_bot.bat", "w") as f:
        f.write(f"@echo off\\n")
        f.write(f"cd {os.getcwd()}\\n")
        f.write(f"venv\\Scripts\\python -m mode_0\\n")
    
    print("\\nTo set up as a service:")
    print("1. Open Task Scheduler")
    print("2. Create a new task")
    print("3. Set it to run at system startup")
    print("4. Add an action to start program: " + os.path.join(os.getcwd(), "run_bot.bat"))
    
    response = input("\\nWould you like to try to set up the service automatically? (y/n): ")
    if response.lower() == 'y':
        try:
            # Use schtasks to create a scheduled task
            task_name = "Mode0Bot"
            batch_path = os.path.join(os.getcwd(), "run_bot.bat")
            
            cmd = f'schtasks /create /tn "{task_name}" /tr "{batch_path}" /sc onstart /ru System'
            subprocess.check_call(cmd, shell=True)
            
            print(f"Windows task '{task_name}' created successfully")
        except subprocess.CalledProcessError:
            print("Error creating Windows task. Please set up manually using the instructions above.")

def setup_linux_service():
    \"\"\"Set up Linux systemd service\"\"\"
    print("Setting up Linux systemd service...")
    
    # Create service file
    service_content = f\"\"\"[Unit]
Description=Mode_0 Twitch Bot
After=network.target

[Service]
Type=simple
User={os.getlogin()}
WorkingDirectory={os.getcwd()}
ExecStart={os.getcwd()}/venv/bin/python -m mode_0
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
\"\"\"
    
    service_path = os.path.join(os.getcwd(), "mode_0.service")
    with open(service_path, "w") as f:
        f.write(service_content)
    
    print(f"Service file created at {service_path}")
    print("\\nTo install the service:")
    print(f"sudo cp {service_path} /etc/systemd/system/")
    print("sudo systemctl daemon-reload")
    print("sudo systemctl enable mode_0.service")
    print("sudo systemctl start mode_0.service")
    
    response = input("\\nWould you like to try to install the service now? (requires sudo) (y/n): ")
    if response.lower() == 'y':
        try:
            subprocess.check_call(["sudo", "cp", service_path, "/etc/systemd/system/"])
            subprocess.check_call(["sudo", "systemctl", "daemon-reload"])
            subprocess.check_call(["sudo", "systemctl", "enable", "mode_0.service"])
            subprocess.check_call(["sudo", "systemctl", "start", "mode_0.service"])
            print("Service installed and started successfully")
        except subprocess.CalledProcessError:
            print("Error installing service. Please install manually using the instructions above.")
        except FileNotFoundError:
            print("Error: sudo command not found. Please install manually using the instructions above.")

def create_data_dirs():
    \"\"\"Create necessary data directories\"\"\"
    dirs = ["data", "logs"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("Data directories created")

def main():
    \"\"\"Main installation function\"\"\"
    print("Mode_0 Twitch Bot - Installation")
    print("===============================")
    
    # Check Python version
    check_python_version()
    
    # Setup venv
    setup_venv()
    
    # Install dependencies
    install_dependencies()
    
    # Create data directories
    create_data_dirs()
    
    # Setup configuration
    setup_config()
    
    # Setup service
    response = input("Would you like to set up the bot as a system service? (y/n): ")
    if response.lower() == 'y':
        setup_service()
    
    print("\\nInstallation complete!")
    print("You can now run the bot with:")
    if platform.system() == "Windows":
        print("venv\\Scripts\\python -m mode_0")
    else:
        print("venv/bin/python -m mode_0")

if __name__ == "__main__":
    main()
"""},
    
    {"path": "scripts/backup.py", "content": """#!/usr/bin/env python3
\"\"\"
Backup script for Mode_0 Twitch Bot.
Creates a backup of the database and configuration files.
\"\"\"
import os
import sys
import shutil
import datetime
import argparse
import zipfile

def create_backup(output_dir=None, include_logs=False):
    \"\"\"Create a backup of the bot data\"\"\"
    # Get timestamp for backup name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Set default output directory if not specified
    if not output_dir:
        output_dir = "backups"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up backup filename
    backup_file = os.path.join(output_dir, f"mode_0_backup_{timestamp}.zip")
    
    # Files and directories to backup
    backup_items = [
        "mode_0/config/config.json",
        "mode_0/config/persona_config.json",
        "mode_0/config/responses.json",
        "data"
    ]
    
    # Add logs if requested
    if include_logs:
        backup_items.append("logs")
    
    # Create zip archive
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in backup_items:
            if os.path.exists(item):
                if os.path.isfile(item):
                    zipf.write(item)
                    print(f"Added file: {item}")
                else:
                    for root, dirs, files in os.walk(item):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path)
                            print(f"Added file: {file_path}")
    
    print(f"\\nBackup created: {backup_file}")
    return backup_file

def restore_backup(backup_file, force=False):
    \"\"\"Restore from a backup file\"\"\"
    if not os.path.exists(backup_file):
        print(f"Error: Backup file {backup_file} not found")
        return False
    
    # Check if current data exists and confirm overwrite
    if not force and (os.path.exists("data") or os.path.exists("mode_0/config/config.json")):
        response = input("Warning: This will overwrite existing data. Continue? (y/n): ")
        if response.lower() != 'y':
            print("Restoration cancelled")
            return False
    
    # Create temporary extraction directory
    temp_dir = "temp_restore"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # Extract backup
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall(temp_dir)
        
        # Restore config files
        config_files = [
            "mode_0/config/config.json",
            "mode_0/config/persona_config.json",
            "mode_0/config/responses.json"
        ]
        
        for config_file in config_files:
            temp_config = os.path.join(temp_dir, config_file)
            if os.path.exists(temp_config):
                # Ensure directory exists
                os.makedirs(os.path.dirname(config_file), exist_ok=True)
                # Copy file
                shutil.copy2(temp_config, config_file)
                print(f"Restored: {config_file}")
        
        # Restore data directory
        temp_data = os.path.join(temp_dir, "data")
        if os.path.exists(temp_data):
            if os.path.exists("data"):
                shutil.rmtree("data")
            shutil.copytree(temp_data, "data")
            print("Restored: data directory")
        
        # Restore logs if they exist in backup
        temp_logs = os.path.join(temp_dir, "logs")
        if os.path.exists(temp_logs):
            if os.path.exists("logs"):
                shutil.rmtree("logs")
            shutil.copytree(temp_logs, "logs")
            print("Restored: logs directory")
        
        print("\\nRestore completed successfully")
        return True
    
    except Exception as e:
        print(f"Error during restore: {e}")
        return False
    
    finally:
        # Clean up temp directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def main():
    \"\"\"Main function\"\"\"
    parser = argparse.ArgumentParser(description="Backup and restore Mode_0 bot data")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create a backup")
    backup_parser.add_argument("-o", "--output", help="Output directory for backup")
    backup_parser.add_argument("-l", "--logs", action="store_true", help="Include logs in backup")
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore from a backup")
    restore_parser.add_argument("file", help="Backup file to restore from")
    restore_parser.add_argument("-f", "--force", action="store_true", help="Force restore without confirmation")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available backups")
    list_parser.add_argument("-d", "--directory", default="backups", help="Directory containing backups")
    
    args = parser.parse_args()
    
    if args.command == "backup":
        create_backup(args.output, args.logs)
    
    elif args.command == "restore":
        restore_backup(args.file, args.force)
    
    elif args.command == "list":
        if not os.path.exists(args.directory):
            print(f"Backup directory {args.directory} not found")
            return
        
        backups = [f for f in os.listdir(args.directory) if f.startswith("mode_0_backup_") and f.endswith(".zip")]
        
        if not backups:
            print(f"No backups found in {args.directory}")
            return
        
        print(f"Available backups in {args.directory}:")
        for backup in sorted(backups):
            backup_path = os.path.join(args.directory, backup)
            size = os.path.getsize(backup_path) / (1024 * 1024)  # Convert to MB
            print(f"  {backup} ({size:.2f} MB)")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
"""},
    
    # Tests
    {"path": "tests/__init__.py", "content": ""},
    
    {"path": "tests/test_bot.py", "content": """\"\"\"
Unit tests for Mode_0 bot core functionality.
\"\"\"
import unittest
import asyncio
import os
import json
from unittest.mock import MagicMock, patch

# Mock config for testing
TEST_CONFIG = {
    "twitch": {
        "oauth_token": "test_token",
        "channel": "test_channel"
    },
    "streamelements": {
        "jwt": "test_jwt",
        "channel_id": "test_channel_id"
    },
    "bot": {
        "name": "TestBot",
        "command_prefix": "!",
        "admin_users": ["admin_user_id"]
    },
    "database": {
        "path": ":memory:"  # Use in-memory SQLite for testing
    }
}

class TestBotCore(unittest.TestCase):
    \"\"\"Test cases for bot core functionality\"\"\"
    
    @classmethod
    def setUpClass(cls):
        # Create a temporary config file for testing
        os.makedirs("mode_0/config", exist_ok=True)
        with open("mode_0/config/test_config.json", "w") as f:
            json.dump(TEST_CONFIG, f)
    
    @classmethod
    def tearDownClass(cls):
        # Clean up
        if os.path.exists("mode_0/config/test_config.json"):
            os.remove("mode_0/config/test_config.json")
    
    def test_config_loading(self):
        \"\"\"Test configuration loading\"\"\"
        from mode_0.config.config_manager import ConfigManager
        
        config = ConfigManager("mode_0/config/test_config.json")
        self.assertEqual(config.get("twitch.channel"), "test_channel")
        self.assertEqual(config.get("bot.command_prefix"), "!")
        self.assertEqual(config.get("nonexistent.key", "default"), "default")
    
    @patch("mode_0.database.db_manager.sqlite3")
    def test_database_setup(self, mock_sqlite):
        \"\"\"Test database initialization\"\"\"
        from mode_0.database.db_manager import DatabaseManager
        
        # Configure mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Create database manager
        db = DatabaseManager(":memory:")
        
        # Verify tables creation was attempted
        self.assertEqual(mock_cursor.execute.call_count, 3)
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

# More test cases would be added here
"""},
    
    {"path": "tests/test_persona.py", "content": """\"\"\"
Unit tests for the persona system.
\"\"\"
import unittest
import json
from unittest.mock import MagicMock, patch

class TestPersonaSystem(unittest.TestCase):
    \"\"\"Test cases for persona system\"\"\"
    
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
        \"\"\"Test greeting generation\"\"\"
        with self.open_patch:
            from mode_0.persona.persona_system import PersonaSystem
            persona = PersonaSystem(self.mock_db)
            
            # Override responses directly
            persona.responses = self.test_responses
            
            # Test greeting
            greeting = asyncio.run(persona.generate_greeting("testuser", "user123"))
            self.assertEqual(greeting, "Hey there, testuser!")
    
    def test_response_generation(self):
        \"\"\"Test response generation\"\"\"
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
"""},
    
    # Docs
    {"path": "docs/README.md", "content": """# Mode_0 Bot Documentation

## Overview

Mode_0 is a custom Twitch bot designed specifically for DJ Qwazi905's channel. The bot integrates with StreamElements for game interactions, features an intelligent chat engagement system, and includes a persona-based memory system for engaging with viewers.

## Architecture

The bot is built with a modular architecture:

- **Core**: Handles Twitch API integration and message processing
- **Persona**: Manages bot personality, responses, and user profiling
- **StreamElements**: Integrates with StreamElements for commands and games
- **Database**: Stores user data, messages, and conversation history
- **Utils**: Provides helper functions and utilities
- **Config**: Manages configuration and settings

## Setup Guide

1. **Installation**
   - Run `scripts/install.py` to set up the project
   - This creates a virtual environment and installs dependencies
   
2. **Configuration**
   - Edit `mode_0/config/config.json` with your credentials
   - Customize `mode_0/config/responses.json` for bot messages
   - Adjust `mode_0/config/persona_config.json` for personality settings
   
3. **Running the Bot**
   - Activate the virtual environment
   - Run `python -m mode_0` to start the bot
   - For production, configure as a service using the installation script

## Key Features

### Intelligent Chat Engagement
- Maintains profiles for each chat user
- Remembers previous interactions
- Generates contextual responses
- Initiates conversations during quiet periods

### StreamElements Integration
- Connects to StreamElements API
- Categorizes and manages chat games
- Tracks points and rewards
- Reacts to events (follows, subs, etc.)

### Persona System
- Customizable bot personality
- Dynamic response generation
- Adapts tone based on chat mood
- Learns from interactions

## Command Reference

### User Commands
- `!help`: Display available commands
- `!about`: Show bot information
- `!socials`: Display DJ Qwazi905's social media links

### Admin Commands
- `!botmode <mode>`: Change bot behavior mode
- More admin commands to be added

## Development

### Adding New Features
1. Implement in the appropriate module
2. Add tests for new functionality
3. Update documentation

### Project Structure
- `mode_0/`: Main package directory
  - `core/`: Core bot functionality
  - `persona/`: Personality and user profiling
  - `streamelements/`: StreamElements integration
  - `database/`: Data storage
  - `utils/`: Helper functions
  - `config/`: Configuration files
- `scripts/`: Utility scripts
- `tests/`: Unit tests
- `logs/`: Log files
- `data/`: Database and data files

## Troubleshooting

### Common Issues
- **Authentication Errors**: Verify Twitch OAuth token and StreamElements JWT
- **Database Errors**: Check file permissions
- **Connection Issues**: Verify network connectivity

### Logs
- Check `logs/` directory for detailed logs
- Standard log level is INFO
- Adjust in config.json for more verbose logging

## Backup and Restore

Use the backup script to manage your data:

```bash
# Create a backup
python scripts/backup.py backup

# Restore from a backup
python scripts/backup.py restore backups/mode_0_backup_20230101_120000.zip

# List available backups
python scripts/backup.py list
```
"""},
    
    # Create a .venv-info file as a placeholder for virtual environment 
    {"path": "venv/.venv-info", "content": """This directory will contain the Python virtual environment.
Run the installation script to create it:

python scripts/install.py
"""}
]


def create_project_structure():
    """Create the project directory structure and files"""
    print(f"Creating project structure for {PROJECT_NAME}...")
    
    # Create directories
    for directory in DIRECTORIES:
        dir_path = directory
        if dir_path and not os.path.exists(dir_path):
            print(f"Creating directory: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
    
    # Create files
    for file_info in FILES:
        file_path = file_info["path"]
        content = file_info["content"]
        
        # Ensure directory exists
        dir_name = os.path.dirname(file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        
        print(f"Creating file: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    # Make scripts executable on Unix-like systems
    if platform.system() != "Windows":
        script_files = [
            "scripts/install.py",
            "scripts/backup.py"
        ]
        for script in script_files:
            if os.path.exists(script):
                os.chmod(script, 0o755)


def main():
    """Main function to set up the project"""
    print("Mode_0 Bot Project Setup")
    print("=======================")
    
    create_project_structure()
    
    print("\nProject structure created successfully!")
    print("\nNext steps:")
    print("1. Run the installation script to set up dependencies:")
    print("   python scripts/install.py")
    print("2. Configure the bot by editing:")
    print("   mode_0/config/config.json")
    print("3. Run the bot:")
    print("   python -m mode_0")


if __name__ == "__main__":
    main()
