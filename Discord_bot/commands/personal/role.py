import discord
from discord.ext import commands

class ReactRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_role_map = {}  # {message_id: {emoji: role_id}}

    @commands.slash_command(name="react", description="Create a role reaction embed")
    @commands.has_permissions(manage_roles=True)
    async def react(
        self,
        ctx,
        role0: discord.Role,
        role1: discord.Role = None,
        role2: discord.Role = None,
        role3: discord.Role = None,
        role4: discord.Role = None,
        role5: discord.Role = None
    ):

        await ctx.defer()

        roles = [r for r in [role0, role1, role2, role3, role4, role5] if r is not None]
        emojis = ['🩷', '🟥', '🟪', '🟨', '🟩', '🟦']  # You can change these if you want


        if len(roles) > len(emojis):
            await ctx.respond("⚠️ Too many roles. Add more emoji if needed.")
            return

        embed = discord.Embed(
            title="🎨 Choose your color role",
            description="\n".join(f"{emoji} → {role.mention}" for emoji, role in zip(emojis, roles)),
            color=discord.Color.blurple()
        )

        message = await ctx.channel.send(embed=embed)

        # Save role mapping for later reaction handling
        self.message_role_map[message.id] = {emoji: role.id for emoji, role in zip(emojis, roles)}

        # React to message
        for emoji in self.message_role_map[message.id]:
            await message.add_reaction(emoji)

        await ctx.respond("✅ Reaction role message created.", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member is None or payload.member.bot:
            return

        if payload.message_id not in self.message_role_map:
            return

        emoji = str(payload.emoji)
        role_id = self.message_role_map[payload.message_id].get(emoji)
        if not role_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(role_id)
        member = payload.member

        if role and role not in member.roles:
            await member.add_roles(role, reason="Reaction role assignment")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id not in self.message_role_map:
            return

        emoji = str(payload.emoji)
        role_id = self.message_role_map[payload.message_id].get(emoji)
        if not role_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(role_id)
        member = payload.member

        if role and role in member.roles:
            await member.remove_roles(role, reason="Reaction role removal")

def setup(bot):
    bot.add_cog(ReactRoleCog(bot))
