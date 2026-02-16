import time

def register(bot):

    @bot.listener.on_message_event
    async def ping(room, event):
        print(f'event {event}')
        # Ignore our own messages
        if event.sender == bot.creds.username:
            return

        if event.body.strip().lower() == "!ping":
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
