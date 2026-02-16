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

@bot.listener.on_message_event
async def all_commands(room, event):
    match = botlib.MessageMatch(room, event, bot, "!")

    if not match.is_not_from_this_bot():
        return

    cmd = match.command

    # Register once
    rank_plugin = rank.register(bot)
    pp_plugin = pp.register(bot)
    ping_plugin = ping.register(bot)
    echo_plugin = echo.register(bot)
    purge_plugin = purge.register(bot)

    if cmd == "rank":
        await rank_plugin.rank_command(room, event, match)
    elif cmd == "initrank":
        await rank_plugin.initrank_command(room, event, match)
    elif cmd == "removerank":
        await rank_plugin.removerank_command(room, event, match)
    elif cmd == "leaderboard":
        await rank_plugin.leaderboard_command(room, event, match)
    elif cmd == "pp":
        await pp_plugin.pp(room, event, match)
    elif cmd == "ping":
        await ping_plugin.ping(room, event, match)
    elif cmd == "echo":
        await echo_plugin.echo(room, event, match)
    elif cmd == "purge":
        await purge_plugin.purge(room, event, match)

    # Only call if register succeeded and method exists
    if rank_plugin is not None and hasattr(rank_plugin, "on_event"):
        rank_plugin.on_event(room, event)



bot.run()

