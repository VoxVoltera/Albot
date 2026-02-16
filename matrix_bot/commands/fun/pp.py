import random
import simplematrixbotlib as botlib


def register(bot):

    @bot.listener.on_message_event
    async def pp(room, event):
        match = botlib.MessageMatch(room, event, bot, "!")
        
        # Ignore our own messages
        if match.is_not_from_this_bot():

            if match.command("pp") and match.prefix():

                # Extract argument (username) if provided
                args = match.args()
                if len(args) == 0:
                    pp_name = event.sender
                else:
                    pp_name = args[1]

                # Deterministic random based on username
                random.seed(pp_name)
                pp_int = random.randint(1, 51)

                # Special users
                if pp_name == "@voxvoltera:matrix.voxvoltera.com" or pp_name == "@lilleole:matrix.voxvoltera.com":
                    pp_int = 67

                pp_size = f"8{'=' * pp_int}D"

                if pp_int < 18:
                    pp_rating = "smol"
                elif pp_int < 36:
                    pp_rating = "avg"
                elif pp_int < 52:
                    pp_rating = "chungo"
                else:
                    pp_rating = "brainrot"

                message = (
                    f"{pp_name}'s PP size\n\n"
                    f"{pp_size}\n\n"
                    f"*{pp_rating} pp*"
                )

                await bot.api.send_text_message(
                    room.room_id,
                    message
                )

        return
