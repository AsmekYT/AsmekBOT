import logging
import logging.handlers
import sys
import discord
from discord.ext.commands import has_permissions
from discord import Option, Intents
import os
from os.path import join, dirname
from dotenv import load_dotenv
import asyncio

log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
log_handler_file = logging.handlers.RotatingFileHandler(
    filename='asmekbot.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,
    backupCount=5,
)
log_handler_file.setFormatter(log_formatter)
log_handler_stdout = logging.StreamHandler(sys.stdout)
log_handler_stdout.setFormatter(log_formatter)

logging.basicConfig(level=logging.INFO, handlers=[log_handler_file, log_handler_stdout])
logging.getLogger('discord').setLevel(logging.INFO)

log = logging.getLogger(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
log.info(".env file loaded.")

bot_version = "alfa 3.1.2-rewrite"

from functions import database as db
import modal as md
import embed as em
from commands import economy as eco_commands
from commands import utility as util_commands
from commands import moderation as mod_commands

intents = Intents.default()
intents.members = True
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Bot version: {bot_version}')
    print(f'Py-cord version: {discord.__version__}')
    print('Libraries loaded:')
    print(f'- psutil')
    print(f'- mysql-connector-python')
    print('----------------------------------------------------------------')
    print('░█████╗░░██████╗███╗░░░███╗███████╗██╗░░██╗██████╗░░█████╗░████████╗')
    print('██╔══██╗██╔════╝████╗░████║██╔════╝██║░██╔╝██╔══██╗██╔══██╗╚══██╔══╝')
    print('███████║╚█████╗░██╔████╔██║█████╗░░█████═╝░██████╦╝██║░░██║░░░██║░░░')
    print('██╔══██║░╚═══██╗██║╚██╔╝██║██╔══╝░░██╔═██╗░██╔══██╗██║░░██║░░░██║░░░')
    print('██║░░██║██████╔╝██║░╚═╝░██║███████╗██║░╚██╗██████╦╝╚█████╔╝░░░██║░░░')
    print('╚═╝░░╚═╝╚═════╝░╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░')
    print('𝗠𝗮𝗱𝗲 𝗯𝘆 𝗔𝘀𝗺𝗲𝗸𝗬𝗧')
    print('𝗦𝗽𝗲𝗰𝗶𝗮𝗹 𝘁𝗵𝗮𝗻𝗸𝘀 𝘁𝗼 𝗡𝗮𝗱𝘄𝗲𝘆 𝗮𝗻𝗱 𝗦𝘇𝘆𝗺𝘀𝘂𝗻')
    print('----------------------------------------------------------------')
    log.info(f"Bot {bot.user} is ready. Version: {bot_version}")

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"v-{bot_version}"))
    log.info("Bot presence updated.")

    log.info("Checking verification channels...")
    verification_channels_data = await db.fetchall('SELECT channel_id, role_id FROM verification_channels')

    if verification_channels_data:
        required_embed = em.get_server_verification_embed()
        for channel_id, role_id in verification_channels_data:
            channel = bot.get_channel(channel_id)
            if not channel:
                log.warning(f"Verification channel {channel_id} not found.")
                continue

            if not channel.permissions_for(channel.guild.me).read_message_history or \
               not channel.permissions_for(channel.guild.me).send_messages or \
               not channel.permissions_for(channel.guild.me).embed_links:
                log.warning(f"Missing permissions (history/send/embed) in verification channel {channel_id} (guild {channel.guild.id}). Skipping.")
                continue

            try:
                last_message = None
                async for message in channel.history(limit=5):
                    if message.author == bot.user and message.embeds:
                        last_message = message
                        break

                is_correct = False
                if last_message and last_message.embeds:
                    current_embed = last_message.embeds[0]
                    if (current_embed.title == required_embed.title and
                        current_embed.description == required_embed.description and
                        len(current_embed.fields) == len(required_embed.fields) and
                        all(cf.name == rf.name and cf.value == rf.value for cf, rf in zip(current_embed.fields, required_embed.fields))):
                          is_correct = True

                if not is_correct:
                    log.info(f"Verification message incorrect or missing in channel {channel_id}. Purging and resending.")
                    try:
                         await channel.purge(limit=100)
                    except discord.Forbidden:
                         log.error(f"Missing permissions to purge messages in verification channel {channel_id}.")
                         continue
                    except discord.HTTPException as purge_err:
                         log.error(f"Failed to purge verification channel {channel_id}: {purge_err}")
                         continue

                    await channel.send(embed=required_embed)
                    log.info(f"Sent verification message to {channel_id}.")
                else:
                    log.info(f"Verification message in channel {channel_id} is correct. Skipping.")

            except discord.Forbidden:
                log.error(f"Forbidden error checking/updating verification channel {channel_id}.")
            except discord.HTTPException as e:
                log.error(f"HTTPException checking/updating verification channel {channel_id}: {e}")
            except Exception as e:
                log.error(f"Unexpected error with verification channel {channel_id}: {e}", exc_info=True)
    else:
        log.info("No verification channels found in the database.")
    log.info("Verification channel check complete.")


@bot.slash_command(name='work', description='Work and earn some coins!')
async def work(ctx: discord.ApplicationContext):
    await eco_commands.work(ctx)

@bot.slash_command(name='balance', description='Check your current balance.')
async def balance(ctx: discord.ApplicationContext):
    await eco_commands.balance(ctx)

@bot.slash_command(name='loan', description='Manage loans.')
async def loan(ctx: discord.ApplicationContext):
    await eco_commands.loan(ctx)


@bot.slash_command(name='settings', description='Server settings.')
@has_permissions(administrator=True)
async def settings(ctx: discord.ApplicationContext):
    embed_main, view_main = em.get_auto_server_setup_embed_view()
    embed_main.title = "Main Server Settings"
    embed_main.description = "🚧 This section is under construction. 🚧"
    embed_main.fields = []
    await ctx.respond(embed=embed_main, view=view_main, ephemeral=True)


@bot.slash_command(name="clear", description="Clears a specified number of messages from the chat.")
@has_permissions(manage_messages=True)
async def clear(ctx: discord.ApplicationContext, amount: Option(int, "Number of messages to clear", required=True)):
    await mod_commands.clear(ctx, amount)

@bot.slash_command(name='mute', description="Times out a member for a specified duration.")
@has_permissions(moderate_members=True)
async def timeout(ctx: discord.ApplicationContext, member: Option(discord.Member, required=True), reason: Option(str, required=False),
                  days: Option(int, max_value=27, default=0, required=False),
                  hours: Option(int, default=0, required=False), minutes: Option(int, default=0, required=False),
                  seconds: Option(int, default=0, required=False)):
    await mod_commands.timeout(ctx, member, reason, days, hours, minutes, seconds)

@bot.slash_command(name="ban", description="Bans a user from the server.")
@has_permissions(ban_members=True)
async def ban(ctx: discord.ApplicationContext, member: Option(discord.Member, required=True),
              reason: Option(str, "Reason for the ban", required=False)):
    await mod_commands.tempban(ctx, member, 0, reason)


@bot.slash_command(name='ping', description='Checks the bot\'s latency and performance.')
async def ping(ctx: discord.ApplicationContext):
    await util_commands.ping(ctx, bot)

@bot.slash_command(name='version', description='Shows the current bot version.')
async def version(ctx: discord.ApplicationContext):
    await util_commands.version(ctx, bot_version)


@bot.slash_command(name='setverification', description='Sets up the verification channel and role.')
@has_permissions(administrator=True)
async def setverification(ctx: discord.ApplicationContext):
    await ctx.send_modal(md.SetVerificationModal(ctx))

@bot.slash_command(name='verify', description='Verify yourself in the designated verification channel.')
async def verify(ctx: discord.ApplicationContext):
    query = 'SELECT role_id FROM verification_channels WHERE channel_id = %s'
    result = await db.fetchone(query, (ctx.channel.id,))

    if result:
        modal_verify = md.MyModal(ctx, title="Verification")
        await ctx.send_modal(modal_verify)
    else:
        await ctx.respond("This channel is not set up for verification, or verification is disabled.", ephemeral=True)


@bot.slash_command(name="embed", description="Create and send an embed message.")
@has_permissions(manage_messages=True)
async def create_embed(ctx: discord.ApplicationContext):
    view = em.EmbedBuilder(ctx)
    await ctx.respond("Let's create an embed! Use the buttons below.", view=view, ephemeral=True)


if __name__ == "__main__":
    db.initialize_database()

    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        log.critical("BOT TOKEN NOT FOUND IN .env FILE. SHUTTING DOWN.")
        exit()

    if not db.db_pool:
         log.critical("DATABASE CONNECTION POOL FAILED TO INITIALIZE. SHUTTING DOWN.")
         exit()

    log.info("Starting bot...")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        log.critical("LOGIN FAILED: Invalid Token.")
    except Exception as e:
        log.critical(f"An unexpected error occurred during bot execution: {e}", exc_info=True)