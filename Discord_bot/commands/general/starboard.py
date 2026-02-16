import discord
from discord.ext import commands
import asyncio
import json
import os

STARBOARD_FILE = "/data/starboard-posted.json"

class StarBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.posted_message_ids = set()
        self.load_posted_ids()

    def load_posted_ids(self):
        os.makedirs(os.path.dirname(STARBOARD_FILE), exist_ok=True)
        if os.path.exists(STARBOARD_FILE):
            with open(STARBOARD_FILE, "r") as f:
                try:
                    self.posted_message_ids = set(json.load(f))
                except json.JSONDecodeError:
                    self.posted_message_ids = set()
        else:
            self.posted_message_ids = set()

    def save_posted_ids(self):
        with open(STARBOARD_FILE, "w") as f:
            json.dump(list(self.posted_message_ids), f)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.scan_history_for_stars()

    async def scan_history_for_stars(self):
        await self.bot.wait_until_ready()

        for guild in self.bot.guilds:
            starboard_channel = discord.utils.get(guild.text_channels, name="starboard")
            if not starboard_channel:
                continue

            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit=3000):  # Increase if you want deeper scan
                        for reaction in message.reactions:
                            if str(reaction.emoji) == "⭐" and reaction.count >= 3:
                                if message.id in self.posted_message_ids:
                                    continue
                                await self.post_to_starboard(starboard_channel, message, reaction.count)
                except discord.Forbidden:
                    continue

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) != "⭐":
            return

        message = reaction.message
        if message.author.bot or user.bot:
            return

        starboard_channel = discord.utils.get(message.guild.text_channels, name="starboard")
        if not starboard_channel:
            return

        if reaction.count >= 3 and message.id not in self.posted_message_ids:
            await self.post_to_starboard(starboard_channel, message, reaction.count)

    async def post_to_starboard(self, starboard_channel, message, count):
        async for msg in starboard_channel.history(limit=100):
            if msg.embeds:
                try:
                    if msg.embeds[0].footer.text.endswith(str(message.id)):
                        self.posted_message_ids.add(message.id)
                        self.save_posted_ids()
                        return
                except:
                    pass

        content = message.content.strip()
        if not content:
            if message.attachments:
                content = "[Attachment]"
            elif message.embeds:
                content = "[Embedded Content]"
            else:
                content = "*No text content*"

        embed = discord.Embed(
            title=message.author.display_name,
            description=f"{content}\n\n[Jump to post]({message.jump_url})",
            color=discord.Color.gold(),
        )
        embed.set_footer(text=f"⭐ {count} | Message ID: {message.id}")
        embed.timestamp = message.created_at

        if message.attachments:
            embed.set_image(url=message.attachments[0].url)

        await starboard_channel.send(embed=embed)
        self.posted_message_ids.add(message.id)
        self.save_posted_ids()

def setup(bot):
    bot.add_cog(StarBoard(bot))
