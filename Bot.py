import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_ready():
	print(f'Logged as {bot.user}')
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
        embed = discord.Embed(title="Auto server setup", description="Here u can fully set up your discord server with 5 clicks", color=0x001eff)
        embed.add_field(name="----------------------------------------------------------------", value="", inline=False)
        embed.add_field(name="Channels - Click this to create all channels u need on your server", value="", inline=False)
        embed.add_field(name="----------------------------------------------------------------", value="", inline=False)
        embed.add_field(name="Roles - Click this to create all roles u need on your server", value="", inline=False)
        embed.add_field(name="----------------------------------------------------------------", value="", inline=False)
        embed.set_footer(text="AsmekBOT[ALFA] 2023")
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.slash_command(name='settings', description='Settings of the server.')
async def settings(ctx):
    embed = discord.Embed(title="Main server settings", description="Here u can select category with u interested in.", color=0x001eff)
    embed.set_footer(text="AsmekBOT[ALFA] 2023")
    await ctx.respond(embed=embed, view=Button1(), ephemeral=True)

@bot.slash_command(name="clear", description="Komenda umożliwiająca czyszczenie czatu.") 
@has_permissions(manage_messages=True) 
async def clear(ctx, liczba_wiadomości: int): 
    if ctx.channel.type == discord.ChannelType.private: 
        await ctx.respond("Nie możesz używać tej komendy na prywatnej wiadomości.") 
        return 
  
    if liczba_wiadomości <= 0: 
        await ctx.respond("Podaj liczbę wiadomości większą niż 0.") 
        return 
  
    await ctx.channel.purge(limit=liczba_wiadomości) 
  
    embed = discord.Embed(title="Czyszczenie wiadomości", color=0x001eff) 
    embed.add_field(name="Wyczyszczono następującą liczbę wiadomości: ", value=liczba_wiadomości, inline=False) 
    await ctx.respond(embed=embed, delete_after = 5)
    
@bot.slash_command(name='ping', description='Komenda umożliwia sprawdzenie wydajności bota')
async def ping(ctx):
    latency_ms = round(bot.latency * 1000, 1)
    embed=discord.Embed(title="Pong! ", description="Here u can see basic parameters like ping or percent of used cpu. ", color=0x0000ff)
    embed.add_field(name="Ping:", value=f"{latency_ms}ms", inline=True)
    embed.add_field(name="Ping 30s ago:", value="ping2", inline=True)
    embed.add_field(name="Ping 1m ago:", value="ping3", inline=True)
    embed.add_field(name="Ping 5m ago:", value="ping4", inline=True)
    embed.add_field(name="Ping 10m ago:", value="ping5", inline=True)
    embed.add_field(name="Percent of used CPU:", value="cpu", inline=False)
    embed.add_field(name="Percent of used RAM", value="ram", inline=False)
    embed.set_footer(text="AsmekBOT[ALFA]")
    await ctx.respond(embed=embed)

bot.run('YOUR_TOKEN')