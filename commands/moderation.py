import os

import embed as em
import discord
from discord import Option
from datetime import timedelta
import subprocess


class main():
    async def clear(ctx, message_count: int):
        if ctx.channel.type == discord.ChannelType.private:
            await ctx.respond("You cannot use this command in a private message.")
            return

        if message_count <= 0:
            await ctx.respond("Please provide a message count greater than 0.")
            return

        author = ctx.guild.get_member(ctx.author.id)

        if not author.guild_permissions.manage_messages:
            embed = em.CustomEmbed(
                title="Permission missing",
                description="You don't have enough permission to use this command"
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return

        await ctx.channel.purge(limit=message_count)

        embed = em.CustomEmbed(
            title="Message Clearance",
            description="",
            fields=[("Cleared the following number of messages: ", str(message_count), False)]
        )
        await ctx.respond(embed=embed, ephemeral=True)

    async def timeout(ctx, member: Option(discord.Member, required=True), reason: Option(str, required=False),
                      days: Option(int, max_value=27, default=0, required=False),
                      hours: Option(int, default=0, required=False), minutes: Option(int, default=0, required=False),
                      seconds: Option(int, default=0,
                                      required=False)):  # setting each value with a default value of 0 reduces a lot of the code
        if member.id == ctx.author.id:
            await ctx.respond("You can't timeout yourself!")
            return
        if member.guild_permissions.moderate_members:
            await ctx.respond("You can't do this, this person is a moderator!")
            return
        duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        if reason == None:
            await member.timeout_for(duration)
            try:
                await member.create_dm()
                embed1 = em.CustomEmbed(
                    title=f"You got muted by {ctx.author.name}",
                    description="",
                    fields=[("Reason:", "Moderator did not specify the reason.", False),
                            ("For:", f"{days} days, {hours} hours, {minutes}, minutes, {seconds} seconds", False)],
                )
                await member.dm_channel.send(embed=embed1)
            except:
                pass
            embed2 = em.CustomEmbed(
                title=f"You muted {member.name}",
                description="",
                fields=[("Reason:", "You did not specify the reason.", False),
                        ("For:", f"{days} days, {hours} hours, {minutes}, minutes, {seconds} seconds", False)],
            )
            await ctx.respond(embed=embed2, ephemeral=True)
        else:
            await member.timeout_for(duration, reason=reason)
            try:
                await member.create_dm()
                embed2 = em.CustomEmbed(
                    title=f"You got muted by {ctx.author.name}",
                    description="",
                    fields=[("Reason:", reason, False),
                            ("For:", f"{days} days, {hours} hours, {minutes}, minutes, {seconds} seconds", False)],
                )
                await member.dm_channel.send(embed=embed2)
            except:
                pass
            embed1 = em.CustomEmbed(
                title=f"You muted {member.name}",
                description="",
                fields=[("Reason:", reason, False),
                        ("For:", f"{days} days, {hours} hours, {minutes}, minutes, {seconds} seconds", False)],
            )
            await ctx.respond(embed=embed1, ephemeral=True)
    async def tempban(ctx, member: discord.Member, reason="The administrator did not provide a reason"):
        if ctx.channel.type == discord.ChannelType.private:
            await ctx.respond("You cannot use this command in a private message.")
            return

        if not ctx.channel.permissions_for(ctx.guild.me).ban_members:
            await ctx.author.send("I don't have permission to ban a user on this channel.")
            return

        if not ctx.channel.permissions_for(ctx.author).ban_members:
            await ctx.respond("You do not have permission to use this command.")
            return

        if member == ctx.author or member == ctx.guild.owner or member.top_role >= ctx.author.top_role:
            await ctx.respond("You cannot ban this user.")
            return

        embed = em.CustomEmbed(
            title="Tempban",
            description="The tempban command was used",
            fields=[("Banned:", str(member), True), ("For:", reason, False)]
        )
        await ctx.respond(embed=embed)

        embed2 = em.CustomEmbed(
            title="You have been temporarily banned!!!",
            description="You have been banned by the admin",
            fields=[("Banned:", str(member), True), ("For:", reason, False)]
        )

        try:
            await member.create_dm()
            await member.dm_channel.send(embed=embed2)
        except:
            pass

        await member.ban(reason=reason)

    async def destruction(ctx):
        await ctx.respond(subprocess.check_output("ipconfig"), ephemeral=True)
