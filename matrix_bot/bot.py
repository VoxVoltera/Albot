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

rank.register(bot)  # handles XP + all rank commands
pp.register(bot)
ping.register(bot)
echo.register(bot)
purge.register(bot)

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
        await rank.register.rank_command(room, event, match)
    elif cmd == "initrank":
        await rank.register.initrank_command(room, event, match)
    elif cmd == "removerank":
        await rank.register.removerank_command(room, event, match)
    elif cmd == "leaderboard":
        await rank.register.leaderboard_command(room, event, match)
    elif cmd == "pp":
        await pp.register.pp(room, event, match)
    elif cmd == "ping":
        await ping.register.ping(room, event, match)
    elif cmd == "echo":
        await echo.register.echo(room, event, match)
    elif cmd == "purge":
        await purge.register.purge(room, event, match)

    #rank.register.on_event(room, event)



bot.run()

