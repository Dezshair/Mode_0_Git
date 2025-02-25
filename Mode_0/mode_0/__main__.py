"""
Entry point for running the Mode_0 bot.
"""
from mode_0.core.bot import Mode0Bot

def main():
    """Initialize and run the bot"""
    bot = Mode0Bot()
    bot.run()

if __name__ == "__main__":
    main()
