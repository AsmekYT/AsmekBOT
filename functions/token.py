import discord
import random
import string

def generate_random_special_character():
    special_characters = string.punctuation.replace("#", "")
    return random.choice(special_characters)

def generate_random_digits():
    return ''.join(random.choices(string.digits, k=5))

def generate_token(user: discord.User):
    nickname = user.name
    special_char1 = generate_random_special_character()
    special_char2 = generate_random_special_character()
    random_digits = generate_random_digits()
    time_numbers = user.created_at.strftime("%H%M")

    generated_token = f"{nickname}{special_char1}{random_digits}{special_char2}{time_numbers}".upper()
    return generated_token