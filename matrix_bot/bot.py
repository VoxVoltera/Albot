import simplematrixbotlib as botlib
import os
from dotenv import load_dotenv
from commands.admin import ping, echo, purge
from commands.fun import pp
from commands.personal import rank


load_dotenv()

config = botlib.Config()
config.load_toml("/app/conf.toml")

creds = botlib.Creds(
    homeserver=os.getenv("SERVER_URL"),
    username="albot",
    password=os.getenv("PASSWORD"),
    session_stored_file="session.txt"
)

bot = botlib.Bot(
    creds=creds,
    config=config
)

@bot.listener.on_startup
async def room_joined(room_id):
    print(f"This account is a member of a room with the id {room_id}")

ping.register(bot)
purge.register(bot)
echo.register(bot)
pp.register(bot)
#rank.register(bot)

bot.run()

