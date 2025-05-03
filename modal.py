import discord
from functions import database as db
from functions import token as token_utils
import asyncio
import logging

log = logging.getLogger(__name__)

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

    async def callback(self, interaction: discord.Interaction):
        try:
            role_id = int(self.children[0].value)
            channel_id = int(self.children[1].value)
        except ValueError:
            await interaction.response.send_message("Role ID and Channel ID must be numbers.", ephemeral=True)
            return

        guild_id = self.ctx.guild.id

        query_check = 'SELECT 1 FROM verification_channels WHERE guild_id = %s'
        result = await db.fetchone(query_check, (guild_id,))

        if result:
            await interaction.response.send_message(
                "A verification channel is already set for this server. Do you want to overwrite it?",
                view=ConfirmOverwriteView(guild_id, channel_id, role_id),
                ephemeral=True
            )
        else:
            query_insert = 'INSERT INTO verification_channels (guild_id, channel_id, role_id) VALUES (%s, %s, %s)'
            success = await db.execute(query_insert, (guild_id, channel_id, role_id))
            if success:
                await interaction.response.send_message("Verification setup completed!", ephemeral=True)
            else:
                await interaction.response.send_message("Failed to set up verification. Please check logs.", ephemeral=True)


class ConfirmOverwriteView(discord.ui.View):
    def __init__(self, guild_id, channel_id, role_id):
        super().__init__(timeout=180)
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.role_id = role_id

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        query = 'REPLACE INTO verification_channels (guild_id, channel_id, role_id) VALUES (%s, %s, %s)'
        success = await db.execute(query, (self.guild_id, self.channel_id, self.role_id))

        if success:
            await interaction.response.edit_message(content="Verification channel updated successfully!", view=None)
        else:
            await interaction.response.edit_message(content="Failed to update verification channel. Please check logs.", view=None)
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Operation cancelled.", view=None)
        self.stop()


class MyModal(discord.ui.Modal):
    def __init__(self, ctx, *args, **kwargs) -> None:
        self.ctx = ctx
        self.required_token = token_utils.generate_token(ctx.author)
        super().__init__(
            discord.ui.InputText(
                label=f"Retype: {self.required_token}",
                placeholder="Here you must retype this token",
                custom_id="input_text"
            ),
            *args, **kwargs
        )
        self.title = "Verification"

    async def callback(self, interaction: discord.Interaction):
        user_token = self.children[0].value.upper()

        if user_token != self.required_token.upper():
            await interaction.response.send_message("Invalid token. Please try again.", ephemeral=True)
            return

        query = 'SELECT role_id FROM verification_channels WHERE channel_id = %s'
        result = await db.fetchone(query, (self.ctx.channel.id,))

        if result:
            role_id = result[0]
            role = self.ctx.guild.get_role(role_id)
            if role:
                try:
                    await interaction.user.add_roles(role, reason="Verified via command")
                    await interaction.response.send_message("Token verified successfully! Role assigned.", ephemeral=True)
                except discord.Forbidden:
                    log.error(f"Missing permissions to assign role {role_id} in guild {self.ctx.guild.id}")
                    await interaction.response.send_message("I don't have permissions to assign the role. Please contact an administrator.", ephemeral=True)
                except discord.HTTPException as e:
                    log.error(f"Failed to assign role {role_id} in guild {self.ctx.guild.id}: {e}")
                    await interaction.response.send_message("An error occurred while assigning the role.", ephemeral=True)
            else:
                log.warning(f"Role {role_id} not found in guild {self.ctx.guild.id} for verification channel {self.ctx.channel.id}")
                await interaction.response.send_message("Role not found. Please contact an administrator.", ephemeral=True)
        else:
            await interaction.response.send_message("Verification not set up correctly for this channel. Please contact an administrator.", ephemeral=True)


class AddFieldModal(discord.ui.Modal):
    def __init__(self, embed_builder_view):
        self.embed_builder_view = embed_builder_view
        super().__init__(
            discord.ui.InputText(label="Field Name", placeholder="Enter the field name here", custom_id="field_name", max_length=256),
            discord.ui.InputText(label="Field Value", placeholder="Enter the field value here", custom_id="field_value", style=discord.InputTextStyle.paragraph, max_length=1024),
            discord.ui.InputText(label="Inline (True/False)", placeholder="True or False", custom_id="inline", max_length=5),
            title="Add Field"
        )

    async def callback(self, interaction: discord.Interaction):
        field_name = self.children[0].value
        field_value = self.children[1].value
        inline_input = self.children[2].value.lower()

        if inline_input not in ["true", "false"]:
            await interaction.response.send_message("Inline must be 'True' or 'False'.", ephemeral=True)
            return

        inline = inline_input == "true"

        if not field_name or not field_value:
             await interaction.response.send_message("Field Name and Field Value cannot be empty.", ephemeral=True)
             return

        if len(self.embed_builder_view.embed.fields) >= 25:
             await interaction.response.send_message("An embed cannot have more than 25 fields.", ephemeral=True)
             return

        self.embed_builder_view.embed.add_field(name=field_name, value=field_value, inline=inline)
        await interaction.response.send_message("Field added!", ephemeral=True)