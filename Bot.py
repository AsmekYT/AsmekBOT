#wersja bota
bot_version = "**3.1.0 [ALFA]**"

#główne komendy inportujące nakładkę discorda do pliku wykonawczego pythona
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import datetime
import time

#zmienne
intents = discord.Intents.all()
intents.members = True
intents.messages = True

#ustalenie podstaw bota (prefixu) oraz usunięcie domyślnej komendy
client = discord.Bot(intents=intents)

#eventy (aktywujące makra)
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/pomoc or for English /help"))
    print("Status bota ustawiony na słucha /pomoc or for English /help")
    #await client.user.edit(description=f"Witaj! Jestem botem Discord./nVersion: {bot_version}")
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
@client.slash_command(name = "ban", description = "Komenda służąca do permanentnego zbanowania urzytkownika", guild=discord.Object(id=12417128931))
@has_permissions(ban_members=True)
async def ban(ctx, użytkownik : discord.Member, powód="Administrator nie podał powodu"):
    embed=discord.Embed(title="Ban", description="Użyto komendy ban", color=0x0011ff)
    embed.add_field(name="Zbanowano:", value=użytkownik, inline=True)
    embed.add_field(name="Za:", value=powód, inline=False)
    await ctx.respond(embed=embed)
    embed2=discord.Embed(title="Zbanowano cię", description="Zostałeś zbanowany przez admina", color=0x0011ff)
    embed2.add_field(name="Zbanowano:", value=użytkownik, inline=True)
    embed2.add_field(name="Za:", value=powód, inline=False)
    await użytkownik.create_dm()
    await użytkownik.dm_channel.send(embed=embed2)
    await użytkownik.ban(reason=powód)
    
@client.slash_command(name = "kick", description = "Komenda do wurzucenia gracza z serwera.")
@has_permissions(kick_members=True)
async def kick(ctx, użytkownik : discord.Member, powód="Administrator nie podał powodu"):
    await użytkownik.kick(reason=powód)
    embed=discord.Embed(title="Kick", description="Użyto komendy kick", color=0x0011ff)
    embed.add_field(name="Zkickowano:", value=użytkownik, inline=True)
    embed.add_field(name="Za:", value=powód, inline=False)
    await ctx.respond(embed=embed)

#@commands.command()
#async def mute(ctx, member: discord.Member):
    #await member.edit(mute=True)

@client.slash_command(name = "clear", description = "Komenda umożliwiająca czyszczenie czatu")
@has_permissions(manage_messages=True)
async def clear(ctx, liczba_wiadomości: int):
    await ctx.channel.purge(limit=liczba_wiadomości)
    embed = discord.Embed(title="Czyszczenie wiadomości", color=0x00e1ff)
    embed.add_field(name="Wyczyszczono następującą liczbę wiadomości: ", value=liczba_wiadomości, inline=False)
    await ctx.respond(embed=embed, delete_after=5)
    
@client.slash_command(name = "ustawweryfikacje", description = "Chwilowo nie działa")
async def setweryfikacja(ctx):
    msg = await ctx.send("Aby się zweryfikować naciśnij emotkę poniżej")
    await msg.add_reaction('✅')
    await ctx.respond("Stworzono weryfikację!") 

#komendy podstawowe
@client.slash_command(name = "pomoc", description = "Pomoc odnośnie używania bota")
async def pomoc(ctx):
    embed=discord.Embed(title="Pomoc", description="Komendy bota", color=0x0011ff)
    embed.set_author(name="Asmek (autor)")
    embed.add_field(name="Menu", value="(NIebawem)", inline=True)
    await ctx.respond(embed=embed)

@client.slash_command(name = "help", description = "List of all bot commands")
async def help(ctx):
    embed=discord.Embed(title="Pomoc", description="Komendy bota", color=0x0011ff)
    embed.set_author(name="Asmek (autor)")
    embed.add_field(name="Menu", value="(NIebawem)", inline=True)
    await ctx.respond(embed=embed)

@client.slash_command(name = "ping", description = "Sprawdza czy bot reaguje na komendy", guild=discord.Object(id=12417128931))
async def ping(ctx):
    print("Działam(komenda ping)")
    await ctx.respond("Pong!")

#komendy for fun
@client.slash_command(name = "iq", description = "Losuje znaczy pokazuje twoje iq w skali od 50 do 200")
async def iq(ctx):
    number = random.randrange(1, 200)
    embed=discord.Embed(color=0x0011ff)
    embed.add_field(name="Twoje IQ wynosi:", value=number, inline=True)
    await ctx.respond(embed=embed)

@client.command(name = "8ball", description = "Odpowiada na zadane pytanie")
async def ball(ctx, wiadomość):
    spis = ["Tak", "Nie", "Oczywiście", "Jasne!!!", "Jak najbardziej", "jak to?", "Nope", "Nieeeee!!!"]
    #lista_zakazana = [valorant, valo, vl]
    #if lista_zakazana in wiadomość:
        #mute()
    await ctx.respond("na wiadomość o treści `" + wiadomość + "` bot odpowiada: ```" + random.choice(spis) + "```")

#token bota (Na ss lub podczas udostępniana kodu uważać czyli usunąć/zamazać. W przypadku przypadowego udostępnienia natychmiast napisać do: Asmek#4413 na pv z prośbą o zresetowanie tokenu bota)
client.run("OTUzMzkwMTAxODkzODkwMTc5.GTBH6E.6qdzYdZ_sKwx01nh-yUlsm-w7MAYGa5Xfa0Qf8")

time.sleep(10)