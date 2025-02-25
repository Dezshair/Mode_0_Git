"""
Unit tests for Mode_0 bot core functionality.
"""
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
    """Test cases for bot core functionality"""
    
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
        """Test configuration loading"""
        from mode_0.config.config_manager import ConfigManager
        
        config = ConfigManager("mode_0/config/test_config.json")
        self.assertEqual(config.get("twitch.channel"), "test_channel")
        self.assertEqual(config.get("bot.command_prefix"), "!")
        self.assertEqual(config.get("nonexistent.key", "default"), "default")
    
    @patch("mode_0.database.db_manager.sqlite3")
    def test_database_setup(self, mock_sqlite):
        """Test database initialization"""
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
