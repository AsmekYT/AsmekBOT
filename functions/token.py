import discord
import random
import string
import mysql.connector
import database as db

def generate_random_special_character():
    special_characters = string.punctuation.replace("#", "")
    return random.choice(special_characters)


def generate_random_digits():
    return ''.join(random.choices(string.digits, k=7))


def generate_token(user: discord.User):
    nickname_with_tag = f"{user.name}"
    special_char = generate_random_special_character()
    random_digits = generate_random_digits()
    date_numbers = ''.join([char for char in str(user.created_at.date()) if char.isdigit()])

    generated_token = f"{nickname_with_tag}{special_char}{random_digits}{date_numbers}".upper()
    return generated_token

class MyModal(discord.ui.Modal):
    def __init__(self, ctx, *args, **kwargs) -> None:
        self.ctx = ctx
        self.token = self.generate_token(ctx.author)
        super().__init__(
            discord.ui.InputText(
                label=f"Retype: {self.token}",
                placeholder="Here you must retype this token",
                custom_id="input_text"
            ),
            *args, **kwargs
        )
        self.title = "Verification"

    async def callback(self, interaction: discord.Interaction):
        user_token = self.children[0].value.upper()
        required_token = self.token.upper()

        if not self.verify_token(user_token, required_token):
            await interaction.response.send_message("Invalid token. Please try again.", ephemeral=True)
            return

        conn = mysql.connector.connect(**db.mysql_config)
        cursor = conn.cursor()
        cursor.execute('SELECT role_id FROM verification_channels WHERE channel_id = %s', (self.ctx.channel.id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            role_id = result[0]
            role = self.ctx.guild.get_role(role_id)
            if role:
                await self.ctx.author.add_roles(role)
                await interaction.response.send_message("Token verified successfully! Role assigned.", ephemeral=True)
            else:
                await interaction.response.send_message("Role not found. Please contact an administrator.", ephemeral=True)
        else:
            await interaction.response.send_message("Verification not set up correctly. Please contact an administrator.", ephemeral=True)

    def generate_random_special_character(self):
        special_characters = string.punctuation.replace("#", "")
        return random.choice(special_characters)

    def generate_random_digits(self):
        return ''.join(random.choices(string.digits, k=5))

    def generate_token(self, user: discord.User):
        nickname_with_tag = f"{user.name}"
        special_char1 = self.generate_random_special_character()
        special_char2 = self.generate_random_special_character()
        random_digits = self.generate_random_digits()
        time_numbers = user.created_at.strftime("%H%M")

        generated_token = f"{nickname_with_tag}{special_char1}{random_digits}{special_char2}{time_numbers}".upper()
        return generated_token

    def verify_token(self, user_token, required_token):
        return user_token == required_token