import discord
import modal as md
from functions import database as db
import mysql.connector

class CustomEmbed(discord.Embed):
    def __init__(self, title, description, color=0x001eff, footer="AsmekBOT 2024©", fields=None):
        super().__init__(title=title, description=description, color=color)
        self.set_footer(text=footer)
        if fields:
            for name, value, inline in fields:
                self.add_field(name=name, value=value, inline=inline)



class UniversalButtonView(discord.ui.View):
    def __init__(self, label: str, style: discord.ButtonStyle, callback):
        super().__init__()
        self.add_item(discord.ui.Button(label=label, style=style, custom_id=label))
        self.callback = callback

    async def interaction_check(self, interaction: discord.Interaction):
        button = self.children[0]
        if interaction.custom_id == button.custom_id:
            await self.callback(interaction)



class EmbedBuilder(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.embed = CustomEmbed(title="Embed Title", description="Embed Description", color=discord.Color.blue())
        self.fields = []

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This is not your embed to modify!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Add Field", style=discord.ButtonStyle.primary)
    async def add_field(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = md.AddFieldModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Preview Embed", style=discord.ButtonStyle.secondary)
    async def preview_embed(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.embed, ephemeral=True)

    @discord.ui.button(label="Send Embed", style=discord.ButtonStyle.success)
    async def send_embed(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.channel.send(embed=self.embed)
        await interaction.response.send_message("Embed sent!", ephemeral=True)
        self.stop()

#----------------------------------------------------------creating embeds-----------------------------------------------------------------------


async def auto_server_setup(interaction: discord.Interaction):
    embed = CustomEmbed(
        title="Auto server setup",
        description="Here you can fully set up your discord server with 5 clicks",
        fields=[
            ("----------------------------------------------------------------", "", False),
            ("Channels - Click this to create all channels you need on your server", "", False),
            ("----------------------------------------------------------------", "", False),
            ("Roles - Click this to create all roles you need on your server", "", False),
            ("----------------------------------------------------------------", "", False),
        ]
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


async def server_verification_setup(interaction: discord.Interaction):
    embed = CustomEmbed(
        title="Server Verification",
        description="Hey, you can verify yourself here.",
        fields=[("To verify:", "Use the /verify command.", False)]
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)



class ConfirmOverwriteView(discord.ui.View):
    def __init__(self, guild_id, channel_id, role_id):
        super().__init__(timeout=180)
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.role_id = role_id

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        conn = mysql.connector.connect(**db.mysql_config)
        cursor = conn.cursor()
        cursor.execute('REPLACE INTO verification_channels (guild_id, channel_id, role_id) VALUES (%s, %s, %s)',
                       (self.guild_id, self.channel_id, self.role_id))
        conn.commit()
        conn.close()

        await interaction.response.send_message("Verification channel updated successfully!", ephemeral=True)
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.secondary)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Operation cancelled.", ephemeral=True)
        self.stop()