#wersja bota
bot_version = "3.2.7"
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
import schedule


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
@client.slash_command(name="ban", description="Komenda służąca do permanentnego zbanowania użytkownika", guild=discord.Object(id=12417128931)) 
@has_permissions(ban_members=True) 
async def ban(ctx, użytkownik: discord.Member, powód="Administrator nie podał powodu"): 
    if ctx.channel.type == discord.ChannelType.private: 
        await ctx.respond("Nie możesz używać tej komendy na prywatnej wiadomości.") 
        return 

    if not ctx.channel.permissions_for(ctx.guild.me).ban_members: 
        await ctx.author.send("Nie mam uprawnień, aby zbanować użytkownika na tym kanale.") 
        return 

    if not ctx.channel.permissions_for(ctx.author).ban_members: 
        await ctx.respond("Nie masz uprawnień, aby użyć tej komendy.") 
        return 
    
    if użytkownik == ctx.author or użytkownik == ctx.guild.owner or użytkownik.top_role >= ctx.author.top_role:
        await ctx.respond("Nie możesz zbanować tego użytkownika.")
        return

    embed = discord.Embed(title="Ban", description="Użyto komendy ban", color=0x0011ff) 
    embed.add_field(name="Zbanowano:", value=użytkownik, inline=True) 
    embed.add_field(name="Za:", value=powód, inline=False) 
    await ctx.respond(embed=embed) 
    
    embed2 = discord.Embed(title="Zbanowano cię", description="Zostałeś zbanowany przez admina", color=0x0011ff) 
    embed2.add_field(name="Zbanowano:", value=użytkownik, inline=True) 
    embed2.add_field(name="Za:", value=powód, inline=False) 

    try: 
        await użytkownik.create_dm() 
        await użytkownik.dm_channel.send(embed=embed2) 
    except: 
        pass 
    
    await użytkownik.ban(reason=powód) 

@client.slash_command(name="kick", description="Komenda do wyrzucenia gracza z serwera.")  
@has_permissions(kick_members=True) 
async def kick(ctx, użytkownik: discord.Member, powód="Administrator nie podał powodu"):  
    if ctx.channel.type == discord.ChannelType.private: 
        await ctx.respond("Nie możesz używać tej komendy na prywatnej wiadomości.") 
        return 
  
    if not ctx.channel.permissions_for(ctx.guild.me).kick_members: 
        await ctx.author.send("Nie mam uprawnień, aby wyrzucić użytkownika z tego kanału.") 
        return 
  
    if not ctx.channel.permissions_for(ctx.author).kick_members: 
        await ctx.respond("Nie masz uprawnień, aby użyć tej komendy.") 
        return 
    
    if użytkownik == ctx.author:
        await ctx.respond("Nie możesz wyrzucić samego siebie.")
        return
    
    if użytkownik == ctx.guild.owner or użytkownik.top_role >= ctx.author.top_role:
        await ctx.respond("Nie możesz wyrzucić użytkownika o wyższej lub takiej samej roli.")
        return
      
    embed2 = discord.Embed(title="Wyrzucono cię", description="Zostałeś wyrzucony przez admina", color=0x0011ff)  
    embed2.add_field(name="Zkickowano:", value=użytkownik, inline=True)  
    embed2.add_field(name="Za:", value=powód, inline=False)  
    try: 
        await użytkownik.create_dm() 
        await użytkownik.dm_channel.send(embed=embed2) 
    except: 
        pass 
      
    await użytkownik.kick(reason=powód)  
    embed = discord.Embed(title="Kick", description="Użyto komendy kick", color=0x0011ff)  
    embed.add_field(name="Zkickowano:", value=użytkownik, inline=True)  
    embed.add_field(name="Za:", value=powód, inline=False)  
    await ctx.respond(embed=embed) 

@client.slash_command(name="mute", description="Komenda do wyciszenia użytkownika")
@has_permissions(mute_members=True)
async def mute(ctx, użytkownik: discord.Member, duration: str = None):
    if duration is None:
        await ctx.respond("Nie podano czasu trwania wyciszenia.")
        return

    # Konwertujemy podany czas trwania wyciszenia na sekundy
    seconds = await parse_time(duration)
    if seconds == -1:
        await ctx.respond("Nieprawidłowy format czasu trwania wyciszenia.")
        return

    # Tworzymy przerwę dla użytkownika
    await member.create_timeout(seconds)

    # Wysyłamy wiadomość potwierdzającą wyciszenie użytkownika
    await ctx.respond(f"{member.mention} został wyciszony na {duration}.")

async def parse_time(time: str) -> int:
    """Konwertuje czas w formacie Xs, Xm, Xh, Xd na sekundy."""
    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        seconds = int(time[:-1]) * time_dict[time[-1]]
    except (ValueError, KeyError):
        seconds = -1
    return seconds

@client.slash_command(name="clear", description="Komenda umożliwiająca czyszczenie czatu.")
@has_permissions(manage_messages=True)
async def clear(ctx, liczba_wiadomości: int):
    if ctx.channel.type == discord.ChannelType.private:
        await ctx.respond("Nie możesz używać tej komendy na prywatnej wiadomości.")
        return

    if liczba_wiadomości <= 0:
        await ctx.respond("Podaj liczbę wiadomości większą niż 0.")
        return

    await ctx.channel.purge(limit=liczba_wiadomości)

    embed = discord.Embed(title="Czyszczenie wiadomości", color=0x00e1ff)
    embed.add_field(name="Wyczyszczono następującą liczbę wiadomości: ", value=liczba_wiadomości, inline=False)
    await ctx.respond(embed=embed, delete_after = 5) 

@client.slash_command()
async def banlist(ctx):
    ban_list = await ctx.guild.bans()
    banned_users = [f"{user.name}#{user.discriminator} ({user.id})" for ban_entry in ban_list if (user := ban_entry.user)]
    if not banned_users:
        await ctx.send("Brak zbanowanych użytkowników.")
        return
    embed = discord.Embed(title="Lista zbanowanych użytkowników", description="\n".join(banned_users), color=discord.Color.red())
    await ctx.send(embed=embed)

@client.slash_command() 
async def unban(ctx, user: discord.User): 
    await ctx.guild.unban(user)
    await ctx.send(f"Użytkownik {user.mention} został odbanowany.")
    
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

@client.slash_command(name="ping", description="Sprawdza czy bot reaguje na komendy", guild=discord.Object(id=12417128931))
async def ping(ctx):
    print("Działam(komenda ping)")
    await ctx.respond(f"Pong! Ping bota wynosi: {int(client.latency * 1000)}ms!")

#komendy for fun
@client.slash_command(name = "iq", description = "Losuje znaczy pokazuje twoje iq w skali od 50 do 200")
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
    with open('iq_data.json', 'w') as f:
        json.dump(iq_data, f) # Zapisanie danych do pliku Json

@client.slash_command(name="8ball", description="Odpowiada na zadane pytanie")  
async def ball(ctx, wiadomosc: str):  
    spis = ["Tak", "Nie", "Oczywiście", "Jasne!!!", "Jak najbardziej", "jak to?", "Nope", "Nieeeee!!!"]  
    zakazane_slowa = ["valorant", "valo", "vl"]  
  
    # Usuń wszystkie znaki interpunkcyjne i zamień na małe litery  
    wiadomosc = ''.join(c for c in wiadomosc if c not in string.punctuation).lower()  
    if len(wiadomosc) > 75:
        await ctx.respond('Pytanie może mieć maksymalnie 75 znaków.')
        return
  
    # Sprawdź, czy wiadomość zawiera tylko znaki interpunkcyjne lub jest pusta  
    if not any(c.isalpha() for c in wiadomosc):  
        await ctx.respond('Pytanie musi zawierać przynajmniej jedną literę.')  
        return  
  
    for slowo in zakazane_slowa:  
        if slowo in wiadomosc:  
            await ctx.respond("Użyłeś zakazanego wyrazu.")  
            return  
  
    try:  
        with open("8ball_data.json", "r") as f:  
            data = json.load(f)  
    except (FileNotFoundError, json.JSONDecodeError):  
        data = {}  
  
    if wiadomosc in data:  
        odpowiedz = data[wiadomosc]  
    else:  
        odpowiedz = random.choice(spis)  
        data[wiadomosc] = odpowiedz  
        with open("8ball_data.json", "w") as f:  
            json.dump(data, f, indent=4)  
  
    await ctx.respond(f"Na pytanie o treści `{wiadomosc}` bot odpowiada: ```{odpowiedz}```") 

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
@client.slash_command(name = "bal", description = "Sprawdza konto w banku")
async def bal(ctx):
    if not ctx.author.id == ctx.guild.owner_id:
        await ctx.author.send("Nie masz uprawnień do wykonania tej komendy.")
        return
    else:
        with open('economy_data.json', 'r') as f:
            data = json.load(f)
        user_id = str(ctx.author.id)
        if user_id in data:
            embed = discord.Embed(title="Balance", description="Twoja liczba pieniędzy zarówno w banku jak i gotówki", color=0x00bd03)
            embed.set_author(name="Bank")
            money = data[user_id]['money']
            embed.add_field(name="Gotówka:", value=money, inline=False)
            bank = data[user_id]['bank']
            embed.add_field(name="Pieniądze w banku:", value=bank, inline=False)
            loan = data[user_id]['loan']
            embed.add_field(name="Pożyczone pieniądze:", value=loan, inline=False)
            embed.set_footer(text="Pozdrawiamy ASMbank")
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(f"{ctx.author.mention}, nie posiadasz jeszcze żadnych środków na koncie możesz zarobić trochę komendą /work lub wziąść pożyczkę komedą /loan.")

@client.slash_command(name='loan', description='Wypożycz pieniądze')
async def loan(ctx, amount: int):
    user_id = str(ctx.author.id)
    with open('economy_data.json', 'r') as f:
        data = json.load(f)

    # sprawdzamy, czy użytkownik już ma aktywną pożyczkę
    if user_id in data and data[user_id]['loan_active']:
        await ctx.respond('Masz już aktywną pożyczkę.')
        return

    # sprawdzamy, czy kwota jest mniejsza niż 100 000
    if amount > 100000:
        await ctx.respond('Nie można wypożyczyć kwoty większej niż 100 000.')
        return

    # obliczamy odsetki
    interest = int(amount * 0.05)
    total = amount + interest

    # dodajemy pieniądze do salda użytkownika i wartości pożyczki
    if user_id in data:
        data[user_id]['money'] += amount
        data[user_id]['loan'] = total
        data[user_id]['loan_active'] = True
    else:
        data[user_id] = {'money': total, 'bank': 0, 'loan': total, 'loan_active': True}

    # zapisujemy zmiany w pliku JSON
    with open('economy_data.json', 'w') as f:
        json.dump(data, f)

    # dodajemy zadanie do harmonogramu automatycznego spłacania
    rate = total / 30
    client.scheduler.add_job(pay_loan_rate, 'interval', days=1, args=[user_id, rate])

    # wyświetlamy informację o pożyczce
    loan_amount = data[user_id]['loan']
    num_of_rates = 30
    remaining_rates = num_of_rates
    if user_id in data and data[user_id]['loan_active']:
        remaining_rates = round(data[user_id]['loan'] / rate)
    await ctx.respond(f'Wypożyczono {total} monet. Spłacaj w ciągu {num_of_rates} dni. Pozostało {loan_amount} monet (pozostało {remaining_rates} rat).')

async def pay_loan_rate(user_id, rate):
    with open('economy_data.json', 'r') as f:
        data = json.load(f)

    if user_id not in data or not data[user_id]['loan_active']:
        return

    loan_amount = data[user_id]['loan']
    data[user_id]['money'] -= rate
    data[user_id]['loan'] -= rate
    if data[user_id]['loan'] <= 0:
        data[user_id]['loan_active'] = False

    with open('economy_data.json', 'w') as f:
        json.dump(data, f)

#tickety/przyciski/embedy
class TicketView(discord.ui.View):
    def __init__(self, user_id, channel_id):
        super().__init__(timeout=180.0)
        self.user_id = user_id
        self.channel_id = channel_id

    @discord.ui.button(label="Stwórz ticket", style=discord.ButtonStyle.primary)
    async def create_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(self.user_id)

        if member is None:
            await interaction.response.send_message("Nie mogę znaleźć użytkownika.", ephemeral=True)
            return

        category = discord.utils.get(guild.categories, name="Tickety")
        if category is None:
            category = await guild.create_category("Tickety")

        ticket_name = f"{member.display_name}-ticket"
        ticket_overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        ticket_channel = await category.create_text_channel(name=ticket_name, overwrites=ticket_overwrites)

        await interaction.response.send_message(f"Kanał {ticket_channel.mention} został utworzony.", ephemeral=True)
        self.channel_id = ticket_channel.id
        await self.send_close_ticket_button(ticket_channel)
        self.stop()

    async def send_close_ticket_button(self, channel):
        embed = discord.Embed(title="Zamknij ticket", description="Kliknij przycisk, aby zamknąć swój ticket.")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(style=discord.ButtonStyle.danger, label="Zamknij ticket", emoji="🔒", 
                                        custom_id=f"close_ticket_{self.user_id}_{self.channel_id}", 
                                        disabled=False))
        await channel.send(embed=embed, view=view)

    @discord.ui.button(label="Zamknij ticket", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        channel = interaction.channel
        category = channel.category
        await interaction.response.defer()
        await channel.delete()
        if len(category.channels) == 0:
            await category.delete()
        self.stop()

@client.slash_command()
async def ticket(ctx: discord.Interaction):
    view = TicketView(ctx.author.id, None)
    embed = discord.Embed(title="Stwórz ticket", description="Kliknij przycisk, aby stworzyć swój ticket.")
    await ctx.respond(embed=embed, view=view)

#token bota
client.run("")

time.sleep(10)