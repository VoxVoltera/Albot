
class Ping:
    def __init__(self, bot):
        self.bot = bot

    async def echo(self, room, event, match):
        print(f'event {event}')

        message = match.args()
        if len(message) == 0:
            message = 'no message provided'
        message = " ".join(message)
        await self.bot.api.send_text_message(
            room.room_id,
            f"{message}"
        )
        return