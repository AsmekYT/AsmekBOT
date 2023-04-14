#główne komendy inportujące nakładkę discorda do pliku wykonawczego pythona
import discord
from discord.ext import commands
from discord import app_commands 
from discord.ext.commands import has_permissions
import random
import datetime
import time

#zmienne
intents = discord.Intents.all()
intents.members = True
intents.messages = True

#ustalenie podstaw bota (prefixu) oraz usunięcie domyślnej komendy
client = commands.Bot(command_prefix= "a!", intents=intents)
client.remove_command("help")

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False 

#eventy (aktywujące makra)
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a!pomoc"))
    if not self.synced: #check if slash commands have been synced 
        await tree.sync(guild = discord.Object(id=953390101893890179)) 
        self.synced = True
    print("Status bota ustawiony na słucha a!pomoc")
    print("Bot gotowy do użytku")
    
@client.event
async def on_member_join(member):
    kanal = discord.utils.get(member.guild.channels, name="czat")
    await kanal.send(f"{member.mention} wszedł na serwer!!!")

@client.event
async def on_member_remove(member):
    kanal = discord.utils.get(member.guild.channels, name="czat")
    await kanal.send(f"{member.name} wyszedł z serwera!!!")


#komendy administracyjne
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, reason="Administrator nie podał powodu"):
    await member.ban(reason=reason)
    embed=discord.Embed(title="Ban", description="Użyto komendy ban", color=0x0011ff)
    embed.add_field(name="Zbanowano:", value=member, inline=True)
    embed.add_field(name="Za:", value=reason, inline=False)
    await ctx.send(embed=embed)
    
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, reason="Administrator nie podał powodu"):
    await member.kick(reason=reason)
    embed=discord.Embed(title="Kick", description="Użyto komendy kick", color=0x0011ff)
    embed.add_field(name="Zkickowano:", value=member, inline=True)
    embed.add_field(name="Za:", value=reason, inline=False)
    await ctx.send(embed=embed)

@commands.command()
async def mute(ctx, member: discord.Member):
    await member.edit(mute=True)
    
@client.command()
async def setweryfikacja(ctx):
    msg = await ctx.send("Aby się zweryfikować naciśnij emotkę poniżej")
    await msg.add_reaction('✅')

#komendy podstawowe
@client.command()
async def pomoc(ctx):
    embed=discord.Embed(title="Pomoc", description="Komendy bota", color=0x0011ff)
    embed.set_author(name="Asmek (autor)")
    embed.add_field(name="Menu", value="(NIebawem)", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed=discord.Embed(title="Pomoc", description="Komendy bota", color=0x0011ff)
    embed.set_author(name="Asmek (autor)")
    embed.add_field(name="Menu", value="(NIebawem)", inline=True)
    await ctx.send(embed=embed)

@tree.command(guild = discord.Object(id=guild_id), name = 'Ping', description='Sprawdzenie czy bot reaguje') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong!", ephemeral = True) 

@client.command()
async def ping(ctx):
    print("Działam(komenda ping)")
    await ctx.send("Pong!")

#komendy for fun
@client.command()
async def iq(ctx):
    number = random.randrange(1, 200)
    embed=discord.Embed(color=0x0011ff)
    embed.add_field(name="Twoje IQ wynosi:", value=number, inline=True)
    await ctx.send(embed=embed)

@client.command()
async def ball(ctx):
    spis = ["Tak", "Nie", "Oczywiście", "Jasne!!!", "Jak najbardziej", "jak to?", "Nope", "Nieeeee!!!"]
    await ctx.channel.send(random.choice(spis))

client = aclient()
tree = app_commands.CommandTree(client)

#token bota (Na ss lub podczas udostępniana kodu uważać czyli usunąć/zamazać. W przypadku przypadowego udostępnienia natychmiast napisać do: Asmek#4413 na pv z prośbą o zresetowanie tokenu bota)
client.run("OTUzMzkwMTAxODkzODkwMTc5.GTBH6E.6qdzYdZ_sKwx01nh-yUlsm-w7MAYGa5Xfa0Qf8")

time.sleep(10)