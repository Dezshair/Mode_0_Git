"""
Helper functions for the Mode_0 bot.
"""
import random
import time
from datetime import datetime, timedelta

def get_random_delay(min_seconds=1, max_seconds=3):
    """Get random delay for human-like response timing"""
    return random.uniform(min_seconds, max_seconds)

def format_duration(seconds):
    """Format seconds into human-readable duration"""
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
    """Calculate human-readable time since timestamp"""
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
