"""
    Command to purge x amount of messages from channel or user (defaults to current channel).
    Sep 15 2024 @ 17:30
    purge.py v0.5

    Sebastian Lindau-Skands
    slinda24@student.aau.dk
"""

from common_libs import *

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='purge', description='Clears a specified number of messages from the channel')
    async def purge_command(self, ctx, amount: int = 1, message: str = ""):
        if amount <= 0:
            await ctx.respond("You can't purge 0 or less messages.", ephemeral=True, delete_after=3)
            return
        elif amount > 100:
            await ctx.respond("You can't purge more than 100 messages.", ephemeral=True, delete_after=3)
            return

        deleted = await ctx.channel.purge(limit=amount)
        await ctx.respond(f"Deleted {len(deleted)} messages.", ephemeral=True, delete_after=3)
        await ctx.send(f"{message}")

def setup(bot):
    bot.add_cog(Purge(bot))
