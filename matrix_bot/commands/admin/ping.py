import time
import simplematrixbotlib as botlib

def register(bot):

    @bot.listener.on_message_event
    async def ping(room, event):
        print(f'event {event}')
        match = botlib.MessageMatch(room, event, bot, "!")
        # Ignore our own messages
        if match.is_not_from_this_bot():

            if match.command("ping") and match.prefix():
                start_time = time.perf_counter()

                await bot.api.send_text_message(
                    room.room_id,
                    "Pinging..."
                )

                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000

                await bot.api.send_text_message(
                    room.room_id,
                    f"Roundtrip latency: {latency_ms:.2f} ms"
                )
        return
