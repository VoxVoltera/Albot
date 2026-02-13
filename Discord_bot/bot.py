from common_libs import *
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="Ricing hyprland"))

def load_extensions():
    categories = ["Admin", "general", "personal"]
    for i in categories:
        for filename in os.listdir(f'./commands/{i}'):
            if filename.endswith('.py'):
                try:
                    bot.load_extension(f'commands.{i}.{filename[:-3]}')
                except Exception as e:
                    print(f'Failed to load extension: {e}')

load_extensions()

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
