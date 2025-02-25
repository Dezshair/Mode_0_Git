# Mode_0 Bot Documentation

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
