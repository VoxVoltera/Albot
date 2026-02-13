import discord
from discord.ext import commands
from commands.personal.levels import level_storage
import random


def calc_level(xp):
    return int((xp / 42) ** 0.5)  # adjust divisor to tune curve


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        guild_id = message.guild.id
        user_id = message.author.id
        data = level_storage.get_user_data(guild_id, user_id)

        prev_level = calc_level(data["xp"])
        data["xp"] += random.randint(0, 5)
        data["messages"] += 1
        new_level = calc_level(data["xp"])

        level_storage.set_user_data(guild_id, user_id, data)

        if new_level > prev_level:
            await message.channel.send(
                f"🎉 **{message.author.display_name}** just leveled up to **Level {new_level}**!"
            )

    @commands.slash_command(name="rank", description="Shows your current rank")
    async def rank(self, ctx, member: discord.Member = None):
        await ctx.defer()
        guild_id = ctx.guild.id
        member = member or ctx.author
        data = level_storage.get_user_data(guild_id, member.id)
        level = calc_level(data["xp"])
        await ctx.respond(f"**{member.display_name}**\nLevel: `{level}`\nXP: `{data['xp']}`")

    @commands.slash_command(name="initrank", description="Initializes the user's rank")
    @commands.has_permissions(administrator=True)
    async def initrank(self, ctx, member: discord.Member, messages: int):
        await ctx.defer()
        guild_id = ctx.guild.id
        xp = sum(random.randint(0, 5) for _ in range(messages))
        data = {"xp": xp, "messages": messages}
        level_storage.set_user_data(guild_id, member.id, data)
        await ctx.respond(f"✅ Initialized rank for **{member.display_name}** to `{messages}` messages.")

    @commands.slash_command(name="removerank", description="Remove n messages worth of XP from user")
    @commands.has_permissions(administrator=True)
    async def removerank(self, ctx, member: discord.Member, messages: int):
        await ctx.defer()
        guild_id = ctx.guild.id
        data = level_storage.get_user_data(guild_id, member.id)
        data["messages"] = max(0, data["messages"] - messages)
        data["xp"] = max(0, data["xp"] - messages * 3)  # Approximate average XP
        level_storage.set_user_data(guild_id, member.id, data)
        await ctx.respond(f"🗑️ Removed `{messages}` messages from {member.display_name}'s rank.")

    @commands.slash_command(name="leaderboard", description="Show the top 15 users by XP")
    async def leaderboard(self, ctx):
        await ctx.defer()
        guild_id = ctx.guild.id
        data = level_storage.get_all_user_data(guild_id)

        if not data:
            await ctx.respond("No data available.")
            return

        sorted_users = sorted(data.items(), key=lambda x: x[1]["xp"], reverse=True)

        lines = ["```yaml", "Top 15 XP Leaderboard:"]
        for i, (user_id, user_data) in enumerate(sorted_users[:15], start=1):
            try:
                user = await self.bot.fetch_user(int(user_id))
                username = user.name if user else f"UnknownUser:{user_id}"
            except:
                username = f"UnknownUser:{user_id}"

            lines.append(f"{i:2d}. {username} — {user_data['xp']} XP")

        lines.append("```")
        await ctx.respond("\n".join(lines))


def setup(bot):
    bot.add_cog(LevelSystem(bot))
