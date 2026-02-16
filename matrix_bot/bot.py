import simplematrixbotlib as botlib
import os
from dotenv import load_dotenv

load_dotenv()

config = botlib.Config()
config.load_toml("conf.toml")
PREFIX = '/'

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

bot.run()

