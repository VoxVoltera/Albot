"""
    Command to meassure bot latency.
    Sep 14 2024 @ 09:00
    ping.py v2

    Sebastian Lindau-Skands
    slinda24@student.aau.dk
"""

from common_libs import *


class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Meassures roundtrip time")
    async def ping(self, ctx):
        await ctx.respond(f"Pong! Roundtrip was: {round(self.bot.latency * 1000)}ms", ephemeral=True, delete_after=3)

def setup(bot):
    bot.add_cog(ping(bot))