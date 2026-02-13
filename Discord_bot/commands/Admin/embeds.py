"""
    Command to create embeds for official announcements.
    Sep 14 2024 @ 09:00
    embeds.py v2

    Sebastian Lindau-Skands
    slinda24@student.aau.dk
"""

from common_libs import *

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Title"))
        self.add_item(discord.ui.InputText(label="Content", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(color=discord.Color.green(), title=self.children[0].value, description=self.children[1].value)
        msg = await interaction.response.send_message(embeds=[embed])  

class said(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="embed", description="Sends an embed with the provided title and content")
    async def modal_slash(self, ctx: discord.ApplicationContext):
        modal = MyModal(title="'What should i say?'")
        await ctx.send_modal(modal)

def setup(bot):
    bot.add_cog(said(bot))