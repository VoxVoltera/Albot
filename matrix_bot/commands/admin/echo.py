

def register(bot):

    async def echo(room, event, match):
        print(f'event {event}')

        message = match.args()
        if len(message) == 0:
            message = 'no message provided'
        message = " ".join(message)
        await bot.api.send_text_message(
            room.room_id,
            f"{message}"
        )
        return