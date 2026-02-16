import random
from levels import level_storage


def register(bot):

    def calc_level(xp):
        return int((xp / 42) ** 0.5)


    @bot.listener.on_event_event
    async def on_event(room, event):

        # Ignore events from the bot itself
        if event.sender == bot.user_id:
            return

        # Ignore non-text events
        if not hasattr(event, "content"):
            return

        if not hasattr(event.content, "body"):
            return

        room_id = room.room_id
        user_id = event.sender

        data = level_storage.get_user_data(room_id, user_id)

        prev_level = calc_level(data["xp"])

        data["xp"] += random.randint(0, 5)
        data["events"] += 1

        new_level = calc_level(data["xp"])

        level_storage.set_user_data(room_id, user_id, data)

        if new_level > prev_level:
            await bot.api.send_text_event(
                room_id,
                f"🎉 **{user_id}** just leveled up to **Level {new_level}**!"
            )

    @bot.listener.on_event_event
    async def rank_command(room, event):
        if not hasattr(event, "content") or not hasattr(event.content, "body"):
            return

        body = event.content.body.strip()
        if not body.startswith("!rank"):
            return

        room_id = room.room_id
        parts = body.split()
        target_user = parts[1] if len(parts) > 1 else event.sender

        data = level_storage.get_user_data(room_id, target_user)
        if not data:
            data = {"xp": 0, "events": 0}

        level = calc_level(data["xp"])

        await bot.api.send_text_event(
            room_id,
            f"**{target_user}**\nLevel: `{level}`\nXP: `{data['xp']}`"
        )

    @bot.listener.on_event_event
    async def initrank_command(room, event):
        if not hasattr(event, "content") or not hasattr(event.content, "body"):
            return

        body = event.content.body.strip()
        if not body.startswith("!initrank"):
            return

        room_id = room.room_id
        parts = body.split()
        if len(parts) != 3:
            await bot.api.send_text_event(room_id, "Usage: !initrank @user events")
            return

        # Admin check
        if not await is_admin(bot, room_id, event.sender):
            return

        target_user = parts[1]
        events = int(parts[2])

        xp = sum(random.randint(0, 5) for _ in range(events))
        data = {"xp": xp, "events": events}
        level_storage.set_user_data(room_id, target_user, data)

        await bot.api.send_text_event(
            room_id,
            f"✅ Initialized rank for **{target_user}** to `{events}` events."
        )

    @bot.listener.on_event_event
    async def removerank_command(room, event):
        if not hasattr(event, "content") or not hasattr(event.content, "body"):
            return

        body = event.content.body.strip()
        if not body.startswith("!removerank"):
            return

        room_id = room.room_id
        parts = body.split()
        if len(parts) != 3:
            await bot.api.send_text_event(room_id, "Usage: !removerank @user events")
            return

        # Admin check
        if not await is_admin(bot, room_id, event.sender):
            return

        target_user = parts[1]
        events = int(parts[2])

        data = level_storage.get_user_data(room_id, target_user)
        if not data:
            data = {"xp": 0, "events": 0}

        data["events"] = max(0, data["events"] - events)
        data["xp"] = max(0, data["xp"] - events * 3)  # Approx average XP

        level_storage.set_user_data(room_id, target_user, data)

        await bot.api.send_text_event(
            room_id,
            f"🗑️ Removed `{events}` events from {target_user}'s rank."
        )

    @bot.listener.on_event_event
    async def leaderboard_command(room, event):
        if not hasattr(event, "content") or not hasattr(event.content, "body"):
            return

        if not event.content.body.strip().startswith("!leaderboard"):
            return

        room_id = room.room_id
        data = level_storage.get_all_user_data(room_id)

        if not data:
            await bot.api.send_text_event(room_id, "No data available.")
            return

        sorted_users = sorted(data.items(), key=lambda x: x[1]["xp"], reverse=True)

        lines = ["Top 15 XP Leaderboard:"]
        for i, (user_id, user_data) in enumerate(sorted_users[:15], start=1):
            lines.append(f"{i:2d}. {user_id} — {user_data['xp']} XP")

        await bot.api.send_text_event(room_id, "\n".join(lines))

async def is_admin(bot, room_id, user_id):
    try:
        power = await bot.api.get_user_power_level(room_id, user_id)
        return power >= 50  # mod 50 admin 100
    except:
        return False