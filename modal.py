import discord
from functions import database as db
import mysql.connector
import random
import string
import embed
import asyncio




class SetVerificationModal(discord.ui.Modal):
    def __init__(self, ctx, *args, **kwargs) -> None:
        self.ctx = ctx
        super().__init__(
            discord.ui.InputText(
                label="Enter role ID for verification",
                placeholder="Role ID",
                custom_id="role_id_input"
            ),
            discord.ui.InputText(
                label="Enter channel ID for verification",
                placeholder="Channel ID",
                custom_id="channel_id_input"
            ),
            title="Verification setup",
            *args, **kwargs
        )
        self.title = "Set Verification Role and Channel"

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.children[0].value)
        channel_id = int(self.children[1].value)
        guild_id = self.ctx.guild.id

        conn = mysql.connector.connect(**db.mysql_config)
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM verification_channels WHERE guild_id = %s', (guild_id,))
        result = cursor.fetchone()

        if result:
            await interaction.response.send_message(
                "A verification channel is already set for this server. Do you want to overwrite it?",
                view=embed.ConfirmOverwriteView(guild_id, channel_id, role_id),
                ephemeral=True
            )
        else:
            cursor.execute('REPLACE INTO verification_channels (guild_id, channel_id, role_id) VALUES (%s, %s, %s)',
                           (guild_id, channel_id, role_id))
            conn.commit()
            conn.close()
            await interaction.response.send_message("Verification setup completed!", ephemeral=True)



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



class AddFieldModal(discord.ui.Modal):
    def __init__(self, view):
        self.view = view
        super().__init__(
            discord.ui.InputText(label="Field Name", placeholder="Enter the field name here", custom_id="field_name"),
            discord.ui.InputText(label="Field Value", placeholder="Enter the field value here", custom_id="field_value"),
            discord.ui.InputText(label="Inline", placeholder="True/False", custom_id="inline"),
            title="Add Field"
        )

    async def callback(self, interaction: discord.Interaction):
        field_name = self.children[0].value
        field_value = self.children[1].value
        inline = self.children[2].value.lower() == "true"

        self.view.embed.add_field(name=field_name, value=field_value, inline=inline)
        await interaction.response.send_message("Field added!", ephemeral=True)



class AmountModal(discord.ui.Modal):
    def __init__(self):

        super().__init__(title="xdddd")

        xd = discord.ui.InputText(label="xdddd", placeholder="Enter the xdddd", custom_id="xdddd")
        self.add_item(xd)

    async def callback(self, interaction: discord.Interaction):
        amount = self.children[0].value
        return amount

#test uniwersalnego modala
class UniversalModal(discord.ui.Modal):
    def __init__(self, title: str, input_fields: list, future: asyncio.Future):
        super().__init__(title=title)

        self.future = future
        self.input_fields = input_fields
        for field in input_fields:
            discord.ui.InputText(label=field['label'], placeholder=field.get('placeholder', ''))


    async def callback(self, interaction: discord.Interaction):
        responses = {field['label']: self.children[i].value for i, field in enumerate(self.input_fields)}
        self.future.set_result(responses)

#przykładowe użycie
async def ask_info(ctx):
    input_fields = [
        {"label": "Name", "placeholder": "Enter your name"},
        {"label": "Age", "placeholder": "Enter your age"},
        {"label": "Email", "placeholder": "Enter your email"}
    ]

    future = asyncio.Future()
    modal = UniversalModal(title="User Information", input_fields=input_fields, future=future)
    await ctx.send_modal(modal)

    responses = await future
    response_message = "\n".join([f"{label}: {value}" for label, value in responses.items()])
    await ctx.send(f"You entered:\n{response_message}")