"""
Database management for the Mode_0 bot.
"""
import sqlite3
import json
import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("mode_0.database")

class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Create tables
        self.setup_database()
        logger.info(f"Database initialized at {db_path}")
    
    def setup_database(self):
        """Create database tables if they don't exist"""
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
        """Add new user or update existing user"""
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
        """Store message in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO messages (user_id, content, channel, timestamp)
        VALUES (?, ?, ?, ?)
        ''', (user_id, content, channel, datetime.now()))
        
        conn.commit()
        conn.close()
    
    async def get_user_profile(self, user_id):
        """Get user profile data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT profile FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return json.loads(result[0])
        return {}
    
    async def update_user_profile(self, user_id, profile_data):
        """Update user profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE users 
        SET profile = ?
        WHERE user_id = ?
        ''', (json.dumps(profile_data), user_id))
        
        conn.commit()
        conn.close()
