import simplematrixbotlib as botlib
import os
from dotenv import load_dotenv
from commands.admin import ping, echo, purge
from commands.fun import pp
from commands.personal.rank import rank_command, initrank_command,  removerank_command,  leaderboard_command, rank_on_event


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
    config=configeaderboard
)

@bot.listener.on_startup
async def room_joined(room_id):
    print(f"This account is a member of a room with the id {room_id}")

    @bot.listener.on_message_event
    async def all_commands(room, event):
        match = botlib.MessageMatch(room, event, bot, "!")

        if not match.is_not_from_this_bot():
            return

        cmd = match.command.lower()

        rank_on_event(room, event)

        if cmd == "rank":
            await rank_command(room, event, match)
        elif cmd == "initrank":
            await initrank_command(room, event, match)
        elif cmd == "removerank":
            await removerank_command(room, event, match)
        elif cmd == "leaderboard":
            await leaderboard_command(room, event, match)

ping.register(bot)
purge.register(bot)
echo.register(bot)
pp.register(bot)

bot.run()

