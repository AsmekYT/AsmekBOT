#główne komendy inportujące nakładkę discorda do pliku wykonawczego pythona
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random

#zmienne
intents = discord.Intents.default()
intents.members = True
intents.messages = True

#ustalenie podstaw bota (prefixu) oraz usunięcie domyślnej komendy
client = commands.Bot(command_prefix= "a!", intents=intents)
client.remove_command("help")

#eventy (aktywujące makra)
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a!pomoc"))
    print("Status bota ustawiony na słucha a!pomoc")
    print("Bot gotowy do użytku (Działa)")
    
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

@client.command()
@commands.has_permissions(mute_members=True)
async def mute(ctx,member: discord.Member, *, reason="Administrator nie podał powodu"):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Zmutowany")
    if not mutedRole:
        mutedRole = await guild.create.role(name="Zmutowany")
        for channel in guild.channels:
            await channel.set_permission(mutedRole, speak=False, send_messages=False, read_message_history=False, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Zmutowano {memeber.metion} za `{reason}`")
    await member.send(f"Zostałeś zmutowany na serwerze `{guild.name} za `{reason}`")
    
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

#token bota
client.run("OTUzMzkwMTAxODkzODkwMTc5.GnwHzI.9AoFbin4furyoj6NjiH6ok1Rhk_ghwEC5xjknI")