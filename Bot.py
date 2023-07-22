bot_version="alfa 3.0.0"

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os
from os.path import join, dirname
from dotenv import load_dotenv
import psutil

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='', intents=intents)

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

class Button1(discord.ui.View):
	@discord.ui.button(label="Auto server setup", style=discord.ButtonStyle.primary)
	async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
		embed = discord.Embed(title="Auto server setup", description="Here you can fully set up your discord server with 5 clicks", color=0x001eff)
		embed.add_field(name="----------------------------------------------------------------", value="", inline=False)
		embed.add_field(name="Channels - Click this to create all channels you need on your server", value="", inline=False)
		embed.add_field(name="----------------------------------------------------------------", value="", inline=False)
		embed.add_field(name="Roles - Click this to create all roles you need on your server", value="", inline=False)
		embed.add_field(name="----------------------------------------------------------------", value="", inline=False)
		embed.set_footer(text="AsmekBOT 2023")
		await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.slash_command(name='settings', description='Settings of the server.')
async def settings(ctx):
	embed = discord.Embed(title="Main server settings", description="Here you can select a category you are interested in.", color=0x001eff)
	embed.set_footer(text="AsmekBOT 2023")
	await ctx.respond(embed=embed, view=Button1(), ephemeral=True)

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
		embed=discord.Embed(title="Permission missing", description="You don't have enough permission to use this command ", color=0x001eff)
		embed.set_footer(text="AsmekBOT 2023")
		await ctx.respond(embed=embed, ephemeral=True)
		return 
	
	await ctx.channel.purge(limit=message_count) 
	
	embed = discord.Embed(title="Message Clearance", color=0x001eff) 
	embed.add_field(name="Cleared the following number of messages: ", value=message_count, inline=False) 
	embed.set_footer(text="AsmekBOT 2023")
	await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name='ping', description='Command to check the bot performance')
async def ping(ctx):
	cpu = psutil.cpu_percent(interval=None)
	ram = psutil.virtual_memory().percent
	latency_ms = round(bot.latency * 1000, 1)
	embed = discord.Embed(title="Pong!", description="Here you can see basic parameters like ping or percent of used CPU.", color=0x0000ff)
	embed.add_field(name="-----------------------------------------------------", value="", inline=False)
	embed.add_field(name="Ping:", value=f"{latency_ms}ms", inline=True)
	embed.add_field(name="-----------------------------------------------------", value="", inline=False)
	embed.add_field(name="Percent of used CPU:", value=f"{cpu}%", inline=False)
	embed.add_field(name="-----------------------------------------------------", value="", inline=False)
	embed.add_field(name="Percent of used RAM", value=f"{ram}%", inline=False)
	embed.add_field(name="-----------------------------------------------------", value="", inline=False)
	embed.set_footer(text="AsmekBOT 2023")
	await ctx.respond(embed=embed)

TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)