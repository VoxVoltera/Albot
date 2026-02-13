from common_libs import *

async def add_members(ctx, role, members, name):
    mem_num = 0
    members_ids = [id.strip().replace("<@", "").replace(">", "") for id in members.split(",")]
    
    for member_id in members_ids:
        member = await ctx.guild.fetch_member(member_id)
        if member:
            await member.add_roles(role)
            mem_num += 1
    
    return 
    
async def dm(ctx, user, message: str):
    try:
        await user.send(message)
        await ctx.respond(f"Sent a DM to {user.name}", ephemeral=True, delete_after=3)  # Acknowledge the interaction
    except Exception as e:
        await ctx.respond(f"Failed to send a DM: {e}", ephemeral=True, delete_after=3) # Acknowledge
