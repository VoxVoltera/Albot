import discord
from discord.ext import commands
#import aiohttp
import random
import httpx

class Gigachad(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    @commands.slash_command(name="gigachad", description="Summon a random gigachad")
    async def gigachad(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get("https://raw.githubusercontent.com/justinlime/GigaChads/main/gigalist.json")
                if resp.status_code != 200:
                    return await ctx.followup.send("Failed to contact the Chad council.")
                data = resp.json()

            gigalist = data["gigachads"]
            chosen = random.choice(gigalist)
            image_url = f"https://raw.githubusercontent.com/justinlime/GigaChads/main/gigachads/{chosen}"
            print(image_url)

            embed = discord.Embed(
                title="Best GigaChad ever:",
                color=discord.Color.green()
            )
            embed.set_image(url=image_url)

            await ctx.followup.send(embed=embed)

        except Exception as e:
            await ctx.respond(f"💥 Error summoning Chad: `{e}`")



def setup(bot):
    bot.add_cog(Gigachad(bot))
