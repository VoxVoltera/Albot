import random
import simplematrixbotlib as botlib


class PP(bot):

    async def pp(room, event, match):

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

        await self.bot.api.send_text_message(
            room.room_id,
            message
        )

        return
