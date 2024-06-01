bot_version = "alfa v3.1.2"

#custom packages
from functions import database as db
import modal as md
import embed as em
from commands import economy as eco
from commands import utility as util
from commands import moderation as mod

#other libralies
import discord
from discord.ext.commands import has_permissions
from discord import Option
import os
from os.path import join, dirname
from dotenv import load_dotenv
import mysql.connector

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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
    print('𝗦𝗽𝗲𝗰𝗶𝗮𝗹 𝘁𝗵𝗮𝗻𝗸𝘀 𝘁𝗼 𝗡𝗮𝗱𝘄𝗲𝘆 𝗮𝗻𝗱 𝗖𝗵𝗶𝗹𝗹𝗰𝗵𝗶𝗹𝗮')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"version: {bot_version}"))

    conn = mysql.connector.connect(**db.mysql_config)
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id FROM verification_channels')
    channels = cursor.fetchall()
    for (channel_id,) in channels:
        channel = bot.get_channel(channel_id)
        if channel:
            last_message = await channel.history(limit=1).flatten()
            if last_message:
                last_message = last_message[0]
                if last_message.embeds:
                    embed = last_message.embeds[0]
                    if (embed.title == "Server Verification" and
                            embed.description == "Hey, you can verify yourself here." and
                            embed.fields[0].name == "To verify:" and
                            embed.fields[0].value == "Use the /verify command."):
                        continue
            await channel.purge()
            await channel.send(embed=em.CustomEmbed(
                title="Server Verification",
                description="Hey, you can verify yourself here.",
                fields=[("To verify:", "Use the /verify command.", False)]
            ))
    conn.close()


@bot.slash_command(name='work', description='Work and earn some coins!')
async def work(ctx):
    await eco.main.work(ctx)


@bot.slash_command(name='balance', description='Check your current balance.')
async def balance(ctx):
    await eco.main.balance(ctx)

@bot.slash_command(name='loan', description='Menage loans.')
async def loan(ctx):
    await eco.main.loan(ctx)


@bot.slash_command(name='settings', description='Settings of the server.')
async def settings(ctx):
    embed = em.CustomEmbed(
        title="Main server settings",
        description="Here you can select a category you are interested in."
    )
    view = em.UniversalButtonView(label="Auto server setup", style=discord.ButtonStyle.primary,
                                  callback=em.auto_server_setup)
    await ctx.respond(embed=embed, view=view, ephemeral=True)


# Moderation commands
@bot.slash_command(name="clear", description="Command to clear chat messages.")
@has_permissions(manage_messages=True)
async def clear(ctx):
    await mod.main.clear(ctx, bot)


@bot.slash_command(name='mute', description="mutes/timeouts a member")
@has_permissions(moderate_members=True)
async def timeout(ctx, member: Option(discord.Member, required=True), reason: Option(str, required=False),
                  days: Option(int, max_value=27, default=0, required=False),
                  hours: Option(int, default=0, required=False), minutes: Option(int, default=0, required=False),
                  seconds: Option(int, default=0,
                                  required=False)):
    await mod.main.timeout(ctx, member, reason, days, hours, minutes, seconds)


@bot.slash_command(name="tempban", description="Command to temporarily ban a user")
@has_permissions(ban_members=True)
async def tempban(ctx, member: discord.Member):
    await mod.main.tempban(ctx, member)


@bot.slash_command(name='ping', description='Command to check the bot performance')
async def ping(ctx):
    await util.main.ping(ctx, bot)


@bot.slash_command(name='version', description='Command to check bot version')
async def version(ctx):
    await util.main.version(ctx, bot_version)


@bot.slash_command(name='setverification', description='Verification setup')
@has_permissions(administrator=True)
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
