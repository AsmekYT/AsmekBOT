import embed as em
import discord
from discord import Option
from datetime import timedelta, datetime, timezone
import logging

log = logging.getLogger(__name__)

async def clear(ctx: discord.ApplicationContext, amount: Option(int, "Number of messages to clear", required=True)):
    if ctx.channel.type == discord.ChannelType.private:
        await ctx.respond("You cannot use this command in a private message.", ephemeral=True)
        return

    if amount <= 0:
        await ctx.respond("Please provide a message count greater than 0.", ephemeral=True)
        return

    if not ctx.app_permissions.manage_messages:
         await ctx.respond("I don't have permission to manage messages in this channel.", ephemeral=True)
         return

    if not ctx.author.guild_permissions.manage_messages:
         await ctx.respond("You don't have permission to use this command.", ephemeral=True)
         return

    try:
        deleted_messages = await ctx.channel.purge(limit=amount)
        confirmation_message = f"Successfully cleared {len(deleted_messages)} messages."

        embed = em.CustomEmbed(
            title="Message Clearance",
            description=confirmation_message,
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed, ephemeral=True, delete_after=10)
    except discord.Forbidden:
        log.warning(f"Missing permissions to clear messages in channel {ctx.channel.id} (guild {ctx.guild.id})")
        await ctx.respond("I don't have the required permissions to delete messages here.", ephemeral=True)
    except discord.HTTPException as e:
        log.error(f"Failed to clear messages in {ctx.channel.id}: {e}")
        await ctx.respond(f"An error occurred while clearing messages: {e}", ephemeral=True)


async def timeout(ctx: discord.ApplicationContext, member: Option(discord.Member, required=True), reason: Option(str, required=False),
                    days: Option(int, max_value=27, default=0, required=False),
                    hours: Option(int, default=0, required=False), minutes: Option(int, default=0, required=False),
                    seconds: Option(int, default=0, required=False)):
    if not ctx.app_permissions.moderate_members:
        await ctx.respond("I don't have permission to timeout members.", ephemeral=True)
        return

    if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself!", ephemeral=True)
        return
    if member.top_role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner_id:
         await ctx.respond("You can't timeout someone with an equal or higher role than you.", ephemeral=True)
         return
    if member.top_role >= ctx.guild.me.top_role:
         await ctx.respond("I can't timeout someone with an equal or higher role than me.", ephemeral=True)
         return
    if member.is_timed_out():
        await ctx.respond(f"{member.mention} is already timed out.", ephemeral=True)
        return

    duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    max_duration = timedelta(days=28)
    if duration <= timedelta(seconds=0):
        await ctx.respond("Please specify a duration greater than 0 seconds.", ephemeral=True)
        return
    if duration > max_duration:
         await ctx.respond("Timeout duration cannot exceed 28 days.", ephemeral=True)
         duration = max_duration

    final_reason = reason if reason else f"Action by {ctx.author.name}#{ctx.author.discriminator}"

    timeout_end_time = discord.utils.utcnow() + duration
    duration_formatted = f"until {discord.utils.format_dt(timeout_end_time, style='F')} ({discord.utils.format_dt(timeout_end_time, style='R')})"

    dm_sent = False
    if member.bot:
        pass
    else:
        try:
            dm_embed = em.CustomEmbed(
                title=f"You have been timed out in {ctx.guild.name}",
                color=discord.Color.orange(),
                fields=[
                    ("Duration:", duration_formatted, False),
                    ("Reason:", final_reason if reason else "No reason provided.", False),
                ]
            )
            await member.send(embed=dm_embed)
            dm_sent = True
        except discord.Forbidden:
            log.warning(f"Could not DM user {member.id} about timeout (Forbidden).")
        except discord.HTTPException as e:
            log.warning(f"Could not DM user {member.id} about timeout (HTTPException: {e}).")

    try:
        await member.timeout(duration, reason=final_reason)

        confirm_embed = em.CustomEmbed(
            title="Member Timed Out",
            color=discord.Color.green(),
            fields=[
                ("Member:", member.mention, True),
                ("Duration:", duration_formatted, True),
                ("Reason:", final_reason if reason else "No reason provided.", False),
                ("DM Sent:", "Yes" if dm_sent else "No (DMs disabled or error)", False)
            ]
        )
        await ctx.respond(embed=confirm_embed, ephemeral=True)

    except discord.Forbidden:
        log.error(f"Missing permissions to timeout member {member.id} in guild {ctx.guild.id}")
        await ctx.respond("I don't have the required permissions to timeout this member.", ephemeral=True)
    except discord.HTTPException as e:
        log.error(f"Failed to timeout member {member.id} in guild {ctx.guild.id}: {e}")
        await ctx.respond(f"An error occurred while trying to timeout the member: {e}", ephemeral=True)


async def tempban(ctx: discord.ApplicationContext, member: Option(discord.Member, required=True),
                  duration_days: Option(int, "Duration of ban in days (0 for permanent)", default=0),
                  reason: Option(str, "Reason for the ban", required=False)):

    if ctx.channel.type == discord.ChannelType.private:
        await ctx.respond("You cannot use this command in a private message.", ephemeral=True)
        return

    if not ctx.app_permissions.ban_members:
        await ctx.respond("I don't have permission to ban members.", ephemeral=True)
        return

    if not ctx.author.guild_permissions.ban_members:
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        return

    if member.id == ctx.author.id:
        await ctx.respond("You cannot ban yourself.", ephemeral=True)
        return
    if member.id == ctx.guild.owner_id:
         await ctx.respond("You cannot ban the server owner.", ephemeral=True)
         return
    if member.top_role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner_id:
        await ctx.respond("You cannot ban someone with an equal or higher role than you.", ephemeral=True)
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.respond("I cannot ban someone with an equal or higher role than me.", ephemeral=True)
        return

    final_reason = reason if reason else f"Action by {ctx.author.name}"
    duration_text = f"{duration_days} days" if duration_days > 0 else "Permanent"

    dm_sent = False
    if not member.bot:
        try:
            embed_dm = em.CustomEmbed(
                title=f"You have been banned from {ctx.guild.name}!",
                description=f"You were banned by {ctx.author.mention}.",
                color=discord.Color.red(),
                fields=[("Duration:", duration_text, True),
                        ("Reason:", final_reason if reason else "No reason provided.", False)]
            )
            await member.send(embed=embed_dm)
            dm_sent = True
        except discord.Forbidden:
            log.warning(f"Could not DM user {member.id} about ban (Forbidden).")
        except discord.HTTPException as e:
            log.warning(f"Could not DM user {member.id} about ban (HTTPException: {e}).")

    try:
        await member.ban(reason=final_reason, delete_message_days=0)

        embed_confirm = em.CustomEmbed(
            title="Member Banned",
            color=discord.Color.dark_red(),
            fields=[
                ("Member:", f"{member.name}#{member.discriminator} ({member.id})", False),
                ("Duration:", duration_text, True),
                ("Reason:", final_reason if reason else "No reason provided.", False),
                ("DM Sent:", "Yes" if dm_sent else "No (DMs disabled or error)", False)
            ]
        )
        await ctx.respond(embed=embed_confirm)

        if duration_days > 0:
            await ctx.send(f"Note: Automatic unban after {duration_days} days is not yet implemented.", ephemeral=True)

    except discord.Forbidden:
        log.error(f"Missing permissions to ban member {member.id} in guild {ctx.guild.id}")
        await ctx.respond("I don't have the required permissions to ban this member.", ephemeral=True)
    except discord.HTTPException as e:
        log.error(f"Failed to ban member {member.id} in guild {ctx.guild.id}: {e}")
        await ctx.respond(f"An error occurred while trying to ban the member: {e}", ephemeral=True)