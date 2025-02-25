"""
Command handlers for Mode_0 bot.
"""
from twitchio.ext import commands
import logging

logger = logging.getLogger("mode_0.core.commands")

class BasicCommands(commands.Cog):
    """Basic bot commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="help")
    async def help_command(self, ctx):
        """Display help information"""
        await ctx.send(f"@{ctx.author.name} Available commands: !help, !about, !socials")
    
    @commands.command(name="about")
    async def about_command(self, ctx):
        """Display information about the bot"""
        await ctx.send(f"@{ctx.author.name} I'm Mode_0, a custom bot for DJ Qwazi905's channel!")
    
    @commands.command(name="socials")
    async def socials_command(self, ctx):
        """Display DJ Qwazi905's social media links"""
        await ctx.send(f"@{ctx.author.name} Follow DJ Qwazi905 on: Twitch: twitch.tv/Qwazi905 | Twitter: x.com/Qwazi905 | SoundCloud: soundcloud.com/qwaziqwazi905")

class AdminCommands(commands.Cog):
    """Admin-only commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="botmode")
    async def mode_command(self, ctx, mode=None):
        """Change bot behavior mode (admin only)"""
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
        """Check if user is an admin"""
        # Implementation to be added
        return False
