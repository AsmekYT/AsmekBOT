#wersja bota
bot_version = "**3.2.4 [ALFA]**"

#główne komendy inportujące nakładkę discorda do pliku wykonawczego pythona
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import datetime
import time
import youtube_dl
import os
import json
import string

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
    embed2=discord.Embed(title="Wyrzucono cię", description="Zostałeś wyrzucony przez admina", color=0x0011ff)
    embed2.add_field(name="Zkickowano:", value=użytkownik, inline=True)
    embed2.add_field(name="Za:", value=powód, inline=False)
    await użytkownik.create_dm()
    await użytkownik.dm_channel.send(embed=embed2)
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
    await ctx.respond(embed=embed, delete_after=10)
    
@client.slash_command(name = "ustawweryfikacje", description = "Chwilowo nie działa")
@commands.is_owner()
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
@client.slash_command(name = "iq", description = "Losuje znaczy pokazuje twoje iq w skali od 50 do 150")
async def iq(ctx):
    user_id = str(ctx.author.id) # Pobranie ID autora komendy
    with open('iq_data.json', 'r') as f:
        iq_data = json.load(f) # Załadowanie danych z pliku JSON
    if user_id not in iq_data:
        iq_data[user_id] = random.randint(50, 150) # Losowanie IQ dla nowego użytkownika
    number = iq_data[user_id] # Pobranie IQ użytkownika
    embed=discord.Embed(color=0x0011ff)
    embed.add_field(name="Twoje IQ wynosi:", value=number, inline=True)
    await ctx.respond(embed=embed)
    with open('iq.json', 'w') as f:
        json.dump(iq_data, f) # Zapisanie danych do pliku Json

@client.command(name="8ball", description="Odpowiada na zadane pytanie")
async def ball(ctx, wiadomość):
    spis = ["Tak", "Nie", "Oczywiście", "Jasne!!!", "Jak najbardziej", "jak to?", "Nope", "Nieeeee!!!"]
    zakazane_slowa = ["valorant", "valo", "vl"]
    for slowo in zakazane_slowa:
        if slowo in wiadomość.lower():
            ctx.respond("Użyłeś zakazanego wyrazu")

    # Usuń interpunkcję i zamień na małe litery
    wiadomość = wiadomość.translate(str.maketrans('', '', string.punctuation)).lower()

    try:
        with open("8ball_data.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if wiadomość in data:
        odpowiedz = data[wiadomość]
    else:
        odpowiedz = random.choice(spis)
        data[wiadomość] = odpowiedz
        with open("8ball_data.json", "w") as f:
            json.dump(data, f, indent=4)

    await ctx.respond("Na pytanie o treści `" + wiadomość + "` bot odpowiada: ```" + odpowiedz + "```")

#komendy muzyczne
@client.slash_command(name = "play", description = "Umożliwia puszczanie muzyki poprzez linki z youtube")
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

#ekonomia
@client.slash_command()
if not command.is_owner():
    await ctx.author.send("Nie masz uprawnień do wykonania tej komendy.")
    return

else:
    async def bal(ctx):
        with open('economy_data.json', 'r') as f:
            data = json.load(f)
        user_id = str(ctx.author.id)
        if user_id in data:
            embed = discord.Embed(title="Balance", description="Twoja liczba pieniędzy zarówno w banku jak i gotówki", color=0x00bd03)
            embed.set_author(name="Bank")
            money = data[user_id]['money']
            embed.add_field(name="Gotówka", value=money, inline=False)
            bank = data[user_id]['bank']
            embed.add_field(name="Pieniądze w banku", value=bank, inline=False)
            loan = data[user_id]['loan']
            embed.add_field(name="Pożyczone pieniądze", value=loan, inline=False)
            embed.set_footer(text="Pozdrawiamy ASMbank")
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(f"{ctx.author.mention}, nie posiadasz jeszcze żadnych środków na koncie możesz zarobić trochę komendą /work lub wziąść pożyczkę komedą /loan.")

#token bota (Na ss lub podczas udostępniana kodu uważać czyli usunąć/zamazać. W przypadku przypadowego udostępnienia natychmiast napisać do: Asmek#4413 na pv z prośbą o zresetowanie tokenu bota)
client.run("OTUzMzkwMTAxODkzODkwMTc5.GTBH6E.6qdzYdZ_sKwx01nh-yUlsm-w7MAYGa5Xfa0Qf8")

time.sleep(10)