from common_libs import *
from common_funcs import dm as dm_func

class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='dm')
    async def dm(self, ctx, user: str, message: str):
        user = await self.bot.fetch_user(int(user.replace("<@", "").replace(">", "")))
        await dm_func(ctx, user, f"{message} - This message can't be replied to")

def setup(bot):
    bot.add_cog(DM(bot))
