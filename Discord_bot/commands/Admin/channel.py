import discord
from discord.ext import commands

class ChannelManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="createchannel", description="Create a channel and post a message in #general")
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self, ctx, name: str, message: str = "Check it out!"):
        await ctx.defer()
        # Create channel
        guild = ctx.guild
        existing = discord.utils.get(guild.channels, name=name)
        if existing:
            await ctx.respond(f"⚠️ Channel `{name}` already exists.")
            return

        channel = await guild.create_text_channel(name)
        general = discord.utils.get(guild.text_channels, name="general")

        if general:
            await general.send(f"created #{name} | {message}")
        await ctx.respond(f"✅ Created channel **#{name}**.", ephemeral=True, delete_after=3)

    @commands.slash_command(name="deletechannel", description="Delete a channel and post a message in #general")
    @commands.has_permissions(manage_channels=True)
    async def deletechannel(self, ctx, name: str, message: str = "Unused"):
        await ctx.defer()
        guild = ctx.guild
        channel = discord.utils.get(guild.text_channels, name=name)

        if not channel:
            await ctx.respond(f"⚠️ Channel `{name}` not found.")
            return

        await channel.delete()
        general = discord.utils.get(guild.text_channels, name="general")

        if general:
            await general.send(f"deleted #{name} | {message}")
        await ctx.respond(f"✅ Deleted channel **#{name}**.", ephemeral=True, delete_after=3)

def setup(bot):
    bot.add_cog(ChannelManager(bot))
