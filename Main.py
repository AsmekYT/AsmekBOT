bot_version = "alfa v3.1.0"

#custom packages
from functions import database as db
import modal as md
import embed as em

#other libralies
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os
from os.path import join, dirname
from dotenv import load_dotenv
import psutil
import random
import mysql.connector
import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#intents = discord.Intents.default()
#intents.messages = True

#bot = commands.Bot(command_prefix='', intents=intents)

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Bot version: {bot_version}')
    print('░█████╗░░██████╗███╗░░░███╗███████╗██╗░░██╗██████╗░░█████╗░████████╗')
    print('██╔══██╗██╔════╝████╗░████║██╔════╝██║░██╔╝██╔══██╗██╔══██╗╚══██╔══╝')
    print('███████║╚█████╗░██╔████╔██║█████╗░░█████═╝░██████╦╝██║░░██║░░░██║░░░')
    print('██╔══██║░╚═══██╗██║╚██╔╝██║██╔══╝░░██╔═██╗░██╔══██╗██║░░██║░░░██║░░░')
    print('██║░░██║██████╔╝██║░╚═╝░██║███████╗██║░╚██╗██████╦╝╚█████╔╝░░░██║░░░')
    print('╚═╝░░╚═╝╚═════╝░╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░')
    print('𝗠𝗮𝗱𝗲 𝗯𝘆 𝗔𝘀𝗺𝗲𝗸𝗬𝗧')
    print('𝗦𝗽𝗲𝗰𝗶𝗮𝗹 𝘁𝗵𝗮𝗻𝗸𝘀 𝘁𝗼 𝗻𝗮𝗱𝘄𝗲𝘆')

    conn = mysql.connector.connect(**db.mysql_config)
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id FROM verification_channels')
    channels = cursor.fetchall()
    for (channel_id,) in channels:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.purge()
            await channel.send(embed=em.CustomEmbed(
                title="Server Verification",
                description="Hey, you can verify yourself here.",
                fields=[("To verify:", "Use the /verify command.", False)]
            ))
    conn.close()



@bot.slash_command(name='settings', description='Settings of the server.')
async def settings(ctx):
    embed = em.CustomEmbed(
        title="Main server settings",
        description="Here you can select a category you are interested in."
    )
    view = em.UniversalButtonView(label="Auto server setup", style=discord.ButtonStyle.primary, callback=em.auto_server_setup)
    await ctx.respond(embed=embed, view=view, ephemeral=True)


# Moderation commands
@bot.slash_command(name="clear", description="Command to clear chat messages.")
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


@bot.slash_command(name="mute", description="Command to mute specific member")
@has_permissions(mute_members=True)
async def mute(ctx, user: discord.Member, duration: str = None):
    if duration is None:
        await ctx.respond("Duration of mute not provided.")
        return

    seconds = await parse_time(duration)
    if seconds == -1:
        await ctx.respond("Invalid mute duration format.")
        return

    await user.timeout(duration=datetime.timedelta(seconds=seconds))

    await ctx.respond(f"{user.mention} has been muted for {duration}.")


async def parse_time(time: str) -> int:
    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        seconds = int(time[:-1]) * time_dict[time[-1]]
    except (ValueError, KeyError):
        seconds = -1
    return seconds


@bot.slash_command(name="tempban", description="Command to temporarily ban a user")
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


@bot.slash_command(name='ping', description='Command to check the bot performance')
async def ping(ctx):
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    latency_ms = round(bot.latency * 1000, 1)
    embed = em.CustomEmbed(
        title="Pong!",
        description="Here you can see basic parameters like ping or percent of used CPU.",
        fields=[
            ("-----------------------------------------------------", "", False),
            ("Ping:", f"{latency_ms}ms", True),
            ("-----------------------------------------------------", "", False),
            ("Percent of used CPU:", f"{cpu}%", False),
            ("-----------------------------------------------------", "", False),
            ("Percent of used RAM", f"{ram}%", False),
            ("-----------------------------------------------------", "", False),
        ]
    )
    await ctx.respond(embed=embed)


@bot.slash_command(name='version', description='Command to check bot version')
async def version(ctx):
    embed = em.CustomEmbed(
        title="Code version",
        description="",
        fields=[
            ("-----------------------------------------------------", "", False),
            ("Bot version:", f"{bot_version}", True),
            ("-----------------------------------------------------", "", False),
        ]
    )
    await ctx.respond(embed=embed)


@bot.slash_command(name='work', description='Work and earn some coins!')
async def work(ctx):
    user_id = ctx.author.id

    conn = mysql.connector.connect(**db.mysql_config)
    cursor = conn.cursor()

    cursor.execute('SELECT last_used FROM cooldowns WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()

    if result is not None:
        last_used = result[0]
        now = datetime.datetime.now()
        cooldown_duration = datetime.timedelta(days=1)
        if now - last_used < cooldown_duration:
            time_left = cooldown_duration - (now - last_used)
            seconds_left = round(time_left.total_seconds())

            hours = seconds_left // 3600
            minutes = (seconds_left % 3600) // 60
            seconds = seconds_left % 60
            time_left_formatted = f'{hours} hours {minutes:02} minutes and {seconds:02} seconds'

            embed = em.CustomEmbed(
                title="Cooldown",
                description="You are on cooldown.",
                fields=[("Time left:", time_left_formatted, False)]
            )
            await ctx.respond(embed=embed, ephemeral=True)
            conn.close()
            return

    earnings = random.randint(1, 100)

    cursor.execute('INSERT INTO wallet (user_id, coins) VALUES (%s, %s) ON DUPLICATE KEY UPDATE coins = coins + %s',
                   (user_id, earnings, earnings))

    cursor.execute('INSERT INTO cooldowns (user_id, last_used) VALUES (%s, %s) ON DUPLICATE KEY UPDATE last_used = %s',
                   (user_id, datetime.datetime.now(), datetime.datetime.now()))

    conn.commit()
    conn.close()

    embed = em.CustomEmbed(
        title='Work',
        description='',
        fields=[('You worked hard and earned:', f'{earnings} coins!', False)]
    )
    await ctx.respond(embed=embed)


@bot.slash_command(name='bal', description='Check your current balance.')
async def balance(ctx):
    user_id = ctx.author.id
    conn = mysql.connector.connect(**db.mysql_config)
    cursor = conn.cursor()

    cursor.execute('SELECT coins FROM wallet WHERE user_id = %s', (user_id,))
    result = cursor.fetchone()

    if result is None:
        balance = 0
    else:
        balance = result[0]

    conn.close()

    embed = em.CustomEmbed(
        title='Balance',
        description='',
        fields=[('Your current balance:', f'{balance} coins', False)]
    )
    await ctx.respond(embed=embed)


@bot.slash_command(name='setverification', description='Verification setup')
async def setverification(ctx):
    await ctx.send_modal(md.SetVerificationModal(ctx))


@bot.slash_command(name='verify', description='Command for verification if command mode is enabled')
async def modal_slash(ctx):
    conn = mysql.connector.connect(**db.mysql_config)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM verification_channels WHERE channel_id = %s', (ctx.channel.id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        modal = md.MyModal(ctx, title="Verification")
        await ctx.send_modal(modal)
    else:
        await ctx.respond("This channel is not set up for verification.", ephemeral=True)


@bot.slash_command(name="embed", description="You can send an embed message by using this command")
async def create_embed(ctx):
    view = em.EmbedBuilder(ctx)
    await ctx.respond("Let's create an embed!", view=view, ephemeral=True)



db.initialize_database()

TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)