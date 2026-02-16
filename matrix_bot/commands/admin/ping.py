import time

class PING(bot):

    async def ping(room, event, match):
        print(f'event {event}')
        start_time = time.perf_counter()

        await self.bot.api.send_text_message(
            room.room_id,
            "Pinging..."
        )

        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000

        await self.bot.api.send_text_message(
            room.room_id,
            f"Roundtrip latency: {latency_ms:.2f} ms"
        )
        return
