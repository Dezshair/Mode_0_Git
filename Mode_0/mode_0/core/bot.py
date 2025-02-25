"""
Core bot implementation for Mode_0.
"""
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
    """Main bot class for Mode_0"""
    
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
        """Register command modules"""
        # To be implemented - register command cogs here
        pass
    
    async def event_ready(self):
        """Called once when bot connects to Twitch"""
        logger.info(f"Bot connected to Twitch | {self.nick}")
        logger.info(f"Connected to channels: {', '.join(self.initial_channels)}")
        
        # Connect to StreamElements
        await self.se_manager.connect()
    
    async def event_message(self, message):
        """Event handler for incoming messages"""
        # Ignore messages from the bot itself
        if message.author is not None and message.author.name.lower() == self.nick.lower():
            return
            
        # Process commands if message starts with prefix
        await self.handle_commands(message)
        
        # Queue message for processing
        if message.author is not None:
            await self.message_queue.put(message)
    
    async def _process_message_queue(self):
        """Process messages from the queue"""
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
        """Initiate conversation when chat is quiet"""
        # Implementation to be added
        pass
