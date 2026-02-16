import time
import simplematrixbotlib as botlib

def register(bot):

    @bot.listener.on_message_event
    async def echo(room, event):
        print(f'event {event}')
        match = botlib.MessageMatch(room, event, bot, "!")
        # Ignore our own messages
        if match.is_not_from_this_bot():
            if match.command("echo") and match.prefix():
                message = match.args()
                if len(message) == 0:
                    message = 'no message provided'
                message = " ".join(message)
                await bot.api.send_text_message(
                    room.room_id,
                    f"{message}"
                )
        return