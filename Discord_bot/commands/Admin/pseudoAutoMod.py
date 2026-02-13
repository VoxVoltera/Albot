import discord
from discord.ext import commands
import json
import os
import time
from datetime import timedelta

BASE_DIR = "data/guilds"

DEFAULT_SETTINGS = {
    "decay_interval": 86400,
    "decay_rate": 1,
    "timeout_minutes": 30,
    "punishments": {
        "5": "warn",
        "10": "timeout",
        "20": "ban"
    }
}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =======================
    # Filesystem helpers
    # =======================

    def guild_dir(self, guild_id: int):
        path = f"{BASE_DIR}/{guild_id}"
        os.makedirs(path, exist_ok=True)
        return path

    def file_path(self, guild_id: int, filename: str):
        return f"{self.guild_dir(guild_id)}/{filename}"

    # =======================
    # JSON helpers
    # =======================

    def load_json(self, guild_id, filename, default):
        path = self.file_path(guild_id, filename)
        if not os.path.exists(path):
            self.save_json(guild_id, filename, default)
        with open(path, "r") as f:
            return json.load(f)

    def save_json(self, guild_id, filename, data):
        with open(self.file_path(guild_id, filename), "w") as f:
            json.dump(data, f, indent=4)

    # =======================
    # Decay logic
    # =======================

    def apply_decay(self, user_data, settings):
        now = time.time()
        elapsed = now - user_data["last_updated"]
        decay = int(elapsed // settings["decay_interval"]) * settings["decay_rate"]
        user_data["points"] = max(0, user_data["points"] - decay)
        user_data["last_updated"] = now
        return user_data

    # =======================
    # Logging
    # =======================

    def log_offence(self, guild_id, member, rule, total_points):
        path = self.file_path(guild_id, "offences.log")
        with open(path, "a") as f:
            f.write(
                f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n"
                f"User: {member} ({member.id})\n"
                f"Rule: {rule['name']} ({rule['points']} points)\n"
                f"Total Points: {total_points}\n"
            )

    # =======================
    # RULE COMMANDS
    # =======================

    @commands.slash_command(name="rule_add", description="Add a rule")
    @commands.has_permissions(administrator=True)
    async def rule_add(self, ctx, section: str, name: str, points: int):
        rules = self.load_json(ctx.guild.id, "rules.json", {})

        rules[section] = {"name": name, "points": points}
        self.save_json(ctx.guild.id, "rules.json", rules)

        await ctx.respond(f"✅ Rule `{section}` added.")

    @commands.slash_command(name="rule_edit", description="Edit a rule")
    @commands.has_permissions(administrator=True)
    async def rule_edit(self, ctx, section: str, name: str, points: int):
        rules = self.load_json(ctx.guild.id, "rules.json", {})

        if section not in rules:
            return await ctx.respond("❌ Rule not found.")

        rules[section] = {"name": name, "points": points}
        self.save_json(ctx.guild.id, "rules.json", rules)

        await ctx.respond(f"✏️ Rule `{section}` updated.")

    @commands.slash_command(name="rule_del", description="Delete a rule")
    @commands.has_permissions(administrator=True)
    async def rule_del(self, ctx, section: str):
        rules = self.load_json(ctx.guild.id, "rules.json", {})

        if section not in rules:
            return await ctx.respond("❌ Rule not found.")

        del rules[section]
        self.save_json(ctx.guild.id, "rules.json", rules)

        await ctx.respond(f"🗑️ Rule `{section}` deleted.")

    @commands.slash_command(name="rule_list", description="List all rules")
    async def rule_list(self, ctx):
        rules = self.load_json(ctx.guild.id, "rules.json", {})

        if not rules:
            return await ctx.respond("No rules configured.")

        embed = discord.Embed(title="Server Rules", color=discord.Color.blue())
        for section, rule in rules.items():
            embed.add_field(
                name=f"Section {section}",
                value=f"{rule['name']} — {rule['points']} points",
                inline=False
            )

        await ctx.respond(embed=embed)

    # =======================
    # SETTINGS
    # =======================

    @commands.slash_command(name="settings_set", description="Update moderation settings")
    @commands.has_permissions(administrator=True)
    async def settings_set(
        self,
        ctx,
        decay_interval: int,
        decay_rate: int,
        timeout_minutes: int
    ):
        settings = self.load_json(
            ctx.guild.id,
            "settings.json",
            DEFAULT_SETTINGS
        )

        settings["decay_interval"] = decay_interval
        settings["decay_rate"] = decay_rate
        settings["timeout_minutes"] = timeout_minutes

        self.save_json(ctx.guild.id, "settings.json", settings)
        await ctx.respond("⚙️ Settings updated.")

    # =======================
    # OFFEND
    # =======================

    @commands.slash_command(name="offend", description="Log an offence")
    @commands.has_permissions(moderate_members=True)
    async def offend(self, ctx, user: discord.Member, section: str):
        await ctx.defer(ephemeral=True)

        gid = ctx.guild.id
        rules = self.load_json(gid, "rules.json", {})
        settings = self.load_json(gid, "settings.json", DEFAULT_SETTINGS)
        infractions = self.load_json(gid, "infractions.json", {})

        if section not in rules:
            return await ctx.followup.send("❌ Unknown rule.")

        rule = rules[section]
        uid = str(user.id)

        if uid not in infractions:
            infractions[uid] = {"points": 0, "last_updated": time.time()}

        infractions[uid] = self.apply_decay(infractions[uid], settings)
        infractions[uid]["points"] += rule["points"]
        total = infractions[uid]["points"]

        # Determine punishment
        punishment = None
        for threshold, action in sorted(
            settings["punishments"].items(),
            key=lambda x: int(x[0]),
            reverse=True
        ):
            if total >= int(threshold):
                punishment = action
                break

        if punishment == "warn":
            await user.send(f"⚠️ Warning: {rule['name']}")
        elif punishment == "timeout":
            await user.timeout(
                discord.utils.utcnow() + timedelta(minutes=settings["timeout_minutes"])
            )
        elif punishment == "ban":
            await user.ban(reason="Exceeded infraction limit")

        self.log_offence(gid, user, rule, total)
        self.save_json(gid, "infractions.json", infractions)

        await ctx.followup.send(
            f"✅ Offence recorded\n"
            f"Points: {total}\n"
            f"Action: {punishment or 'none'}"
        )

def setup(bot):
    bot.add_cog(Moderation(bot))
