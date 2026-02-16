import os
from dotenv import load_dotenv
import simplematrixbotlib as botlib

from commands.admin.ping import Ping
from commands.admin.echo import Echo
from commands.admin.purge import Purge
from commands.fun.pp import Pp
from commands.personal.rank import Rank

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

# Instantiate command handlers (classes)
rank_cmd = Rank(bot)     # handles XP + all rank commands
pp_cmd = Pp(bot)
ping_cmd = Ping(bot)
echo_cmd = Echo(bot)
purge_cmd = Purge(bot)

@bot.listener.on_startup
async def room_joined(room_id):
    print(f"This account is a member of a room with the id {room_id}")

@bot.listener.on_message_event
async def all_commands(room, event):
    match = botlib.MessageMatch(room, event, bot, "!")

    if not match.is_not_from_this_bot():
        return

    cmd = match.command

    if cmd == "rank":
        await rank_cmd.rank_command(room, event, match)
    elif cmd == "initrank":
        await rank_cmd.initrank_command(room, event, match)
    elif cmd == "removerank":
        await rank_cmd.removerank_command(room, event, match)
    elif cmd == "leaderboard":
        await rank_cmd.leaderboard_command(room, event, match)
    elif cmd == "pp":
        await pp_cmd.pp(room, event, match)
    elif cmd == "ping":
        await ping_cmd.ping(room, event, match)
    elif cmd == "echo":
        await echo_cmd.echo(room, event, match)
    elif cmd == "purge":
        await purge_cmd.purge(room, event, match)

bot.run()
