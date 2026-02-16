import asyncio
import simplematrixbotlib as botlib

DEFAULT_LIMIT = 10
MAX_LIMIT = 100


def register(bot):

    @bot.listener.on_message_event
    async def purge(room, event):
        match = botlib.MessageMatch(room, event, bot, "!")
        # Ignore our own messages
        if match.is_not_from_this_bot():

            if match.command("purge") and match.prefix():
                # match.args() is a list in simplematrixbotlib
                args = match.args() or []

                limit = DEFAULT_LIMIT
                if len(args) >= 1:
                    try:
                        limit = int(args[0])
                    except (ValueError, TypeError):
                        await bot.api.send_text_message(
                            room.room_id,
                            "⚠️ Usage: !purge <number> (example: !purge 20)"
                        )
                        return

                # Clamp to safe range
                if limit < 1:
                    limit = 1
                if limit > MAX_LIMIT:
                    limit = MAX_LIMIT

                await bot.api.send_text_message(room.room_id, f"🧹 Purging {limit} message(s)...")

                # Access underlying nio AsyncClient (common in simplematrixbotlib)
                client = bot.api.async_client

                # Start from the current event id if available
                start = getattr(event, "event_id", None)
                if not start and getattr(room, "timeline", None) and room.timeline:
                    start = getattr(room.timeline[-1], "event_id", None)

                if not start:
                    await bot.api.send_text_message(room.room_id, "⚠️ Could not determine where to start in history.")
                    return

                # Fetch a bit more than needed (skip non-message events / command / bot msgs)
                fetch_limit = min(limit + 30, MAX_LIMIT + 30)

                try:
                    resp = await client.room_messages(
                        room_id=room.room_id,
                        start=start,
                        limit=fetch_limit,
                        direction="b",
                    )
                except Exception as e:
                    await bot.api.send_text_message(room.room_id, f"⚠️ Failed to fetch history: {e}")
                    return

                events = getattr(resp, "chunk", []) or []
                if not events:
                    await bot.api.send_text_message(room.room_id, "⚠️ No messages found to purge.")
                    return

                redacted = 0
                bot_user_id = getattr(client, "user_id", None)

                for ev in events:
                    # Skip the command message itself
                    if getattr(ev, "event_id", None) == getattr(event, "event_id", None):
                        continue

                    # Only redact normal room messages
                    if getattr(ev, "type", None) != "m.room.message":
                        continue

                    # Skip the bot's own messages (optional but usually desired)
                    if bot_user_id and getattr(ev, "sender", None) == bot_user_id:
                        continue

                    ev_id = getattr(ev, "event_id", None)
                    if not ev_id:
                        continue

                    try:
                        await client.room_redact(
                            room_id=room.room_id,
                            event_id=ev_id,
                            reason=f"Purged by {getattr(event, 'sender', 'admin')}",
                        )
                        redacted += 1
                        await asyncio.sleep(0.1)  # reduce rate-limit risk
                    except Exception:
                        # keep going if one redact fails (power levels / already redacted / etc.)
                        pass

                    if redacted >= limit:
                        break

                await bot.api.send_text_message(room.room_id, f"✅ Purged {redacted} message(s).")

        return
