import random
from commands.personal.levels import level_storage


class Rank:
    def __init__(self, bot):
        self.bot = bot


    def calc_level(xp):
        return int((xp / 42) ** 0.5)



    async def on_event(self, room, event):


        room_id = room.room_id
        user_id = event.sender

        data = level_storage.get_user_data(room_id, user_id)

        prev_level = self.calc_level(data["xp"])

        data["xp"] += random.randint(0, 5)
        new_level = self.calc_level(data["xp"])
        level_storage.set_user_data(room_id, user_id, data)
        if new_level > prev_level:
            await self.bot.api.send_text_event(
                room_id,
                f"🎉 **{user_id}** just leveled up to **Level {new_level}**!"
            )

    
    async def rank_command(room, event, match):
        room_id = room.room_id

        # Target user: first argument, or fallback to sender
        target_user = match.args[0] if len(match.args) >= 1 else event.sender

        # Get or initialize user data
        data = level_storage.get_user_data(room_id, target_user)
        if not data:
            data = {"xp": 0, "messages": 0}

        level = self.calc_level(data["xp"])

        await self.bot.api.send_text_message(
            room_id,
            f"**{target_user}**\nLevel: `{level}`\nXP: `{data['xp']}`"
        )


    async def initrank_command(self, room, event, match):

                # At this point, match.command.lower() == "initrank"
                # match.args contains a list of arguments
                # Example: "!initrank @user:server 50" -> match.args = ["@user:server", "50"]
        if len(match.args) != 2:
            await self.bot.api.send_text_message(room.room_id, "Usage: !initrank @user messages")
            return

        target_user = match.args[0]
        messages = int(match.args[1])

            # Optional: check admin
        if not await self.is_admin(self.bot, room.room_id, event.sender):
            await self.bot.api.send_text_message(room.room_id, "You need admin to run this command.")
            return

            # Generate XP and store
        xp = sum(random.randint(0, 5) for _ in range(messages))
        data = {"xp": xp, "messages": messages}
        level_storage.set_user_data(room.room_id, target_user, data)

        await self.bot.api.send_text_message(
            room.room_id,
            f"✅ Initialized rank for **{target_user}** to `{messages}` messages."
        )
        print("it worked")


    async def removerank_command(self, room, event, match):

                # At this point, match.command.lower() == "removerank"
                # match.args contains a list of arguments
                # Example: "!removerank @user:server 50" -> match.args = ["@user:server", "50"]
        if len(match.args) != 2:
            await self.bot.api.send_text_event(room.room_id, "Usage: !removerank @user events")
            return


            # Admin check
        if not await self.is_admin(self.bot, room.room_id, event.sender):
            return

        target_user = match.args[0]
        events = int(match.args[1])
        data = level_storage.get_user_data(room.room_id, target_user)
        if not data:
            data = {"xp": 0, "events": 0}

        data["events"] = max(0, data["events"] - events)
        data["xp"] = max(0, data["xp"] - events * 3)  # Approx average XP

        level_storage.set_user_data(room.room_id, target_user, data)

        await self.bot.api.send_text_event(
            room.room_id,
            f"🗑️ Removed `{events}` events from {target_user}'s rank."
        )


    async def leaderboard_command(self, room, event, match):

        room_id = room.room_id
        data = level_storage.get_all_user_data(room_id)

        if not data:
            await self.bot.api.send_text_event(room_id, "No data available.")
            return

        sorted_users = sorted(data.items(), key=lambda x: x[1]["xp"], reverse=True)
        lines = ["Top 15 XP Leaderboard:"]
        for i, (user_id, user_data) in enumerate(sorted_users[:15], start=1):
            lines.append(f"{i:2d}. {user_id} — {user_data['xp']} XP")

        await self.bot.api.send_text_event(room_id, "\n".join(lines))

    async def is_admin(bot, room_id, user_id):
        try:
            power = await bot.api.get_user_power_level(room_id, user_id)
            return power >= 50  # mod 50 admin 100
        except:
            return False