import simplematrixbotlib as botlib
import os
from dotenv import load_dotenv

load_dotenv()

config = botlib.Config()
config.load_toml("conf.toml")

creds = botlib.Creds(
    homeserver=os.getenv("SERVER_URL"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    session_stored_file="session.txt"
    )

bot = botlib.Bot(
    creds=creds,
    config=config
)



bot.run()

