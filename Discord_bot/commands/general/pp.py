import discord
from discord.ext import commands
import random

class pp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="pp",
        description="Showcase the size of your humongous pp"
    )
    async def pp_func(self, ctx: discord.ApplicationContext, user: str = "") -> None:
        if not len(user):
            pp = str(ctx.author)
        else:
            try:
                user_id_int = int(user.strip("<@!>"))
                pp = str(await self.bot.fetch_user(user_id_int))
            except:
                pp = user

        random.seed(pp)
        pp_int = random.randint(1, 51)
        if user == 'lilleole' or user = 'voxvoltera':
            pp_int = 67
        pp_size = f"8{'=' * pp_int}D"
        pp_rating = "smol" if pp_int < 18 else "avg" if pp_int < 36 else "chungo" if pp_int < 52 else "brainrot"

        embed = discord.Embed(
            color=discord.Color.green(),
            title=f"{pp}'s PP size\n\n**{pp_size}**\n\n*{pp_rating} pp*"
        )
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(pp(bot))
