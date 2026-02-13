"""
    Command to reload all command extensions.
    Sep 14 2024 @ 09:00
    update.py v2

    Sebastian Lindau-Skands
    slinda24@student.aau.dk
"""

from common_libs import *

class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  

    @commands.slash_command(name='update', description='Updates specified module')
    async def reload(self, ctx, module):
        try:
            try:
                self.bot.unload_extension(module)
            except:
                print(f"Failed to unload {module}, maybe it wasn't loaded.")
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.respond(f"Error {e}", ephemeral=True, delete_after=3)
            print(f"Failed to reload {module} with exception: {e}")
        else:
            await ctx.respond(f"Done!", ephemeral=True, delete_after=3)
            print(f"Reloaded {module}")

def setup(bot):
    bot.add_cog(Update(bot))