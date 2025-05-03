import discord
import modal as md
from functions import database as db
import logging

log = logging.getLogger(__name__)

class CustomEmbed(discord.Embed):
    def __init__(self, title, description, color=0x001eff, footer="AsmekBOT 2024©", fields=None):
        if len(title) > 256:
            log.warning(f"Embed title longer than 256 characters: '{title[:260]}...'")
            title = title[:256]
        if len(description) > 4096:
            log.warning(f"Embed description longer than 4096 characters: '{description[:100]}...'")
            description = description[:4096]

        super().__init__(title=title, description=description, color=color)
        if footer:
            if len(footer) > 2048:
                log.warning(f"Embed footer longer than 2048 characters: '{footer[:100]}...'")
                footer = footer[:2048]
            self.set_footer(text=footer)

        if fields:
            if len(fields) > 25:
                 log.warning(f"Attempted to create embed with more than 25 fields ({len(fields)}). Truncating.")
                 fields = fields[:25]

            for name, value, inline in fields:
                if len(name) > 256:
                    log.warning(f"Embed field name longer than 256 characters: '{name[:260]}...'")
                    name = name[:256]
                if len(value) > 1024:
                     log.warning(f"Embed field value longer than 1024 characters: '{value[:100]}...'")
                     value = value[:1024]
                self.add_field(name=name, value=value, inline=inline)

class SimpleButton(discord.ui.Button):
    def __init__(self, label: str, style: discord.ButtonStyle, custom_id: str, callback_func):
        super().__init__(label=label, style=style, custom_id=custom_id)
        self.callback_func = callback_func

    async def callback(self, interaction: discord.Interaction):
        await self.callback_func(interaction)

class EmbedBuilder(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.embed = CustomEmbed(title="New Embed Title", description="New Embed Description", color=discord.Color.blue())

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This is not your embed to modify!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Add Field", style=discord.ButtonStyle.primary, row=0)
    async def add_field(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = md.AddFieldModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Preview Embed", style=discord.ButtonStyle.secondary, row=1)
    async def preview_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.embed.title and not self.embed.description and not self.embed.fields:
            await interaction.response.send_message("The embed is empty, nothing to preview.", ephemeral=True)
        else:
            await interaction.response.send_message(embed=self.embed, ephemeral=True)

    @discord.ui.button(label="Send Embed", style=discord.ButtonStyle.success, row=1)
    async def send_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.embed.title and not self.embed.description and not self.embed.fields:
            await interaction.response.send_message("Cannot send an empty embed.", ephemeral=True)
            return

        try:
            await interaction.response.defer(ephemeral=True, thinking=False)
            await interaction.followup.send(embed=self.embed)
            await interaction.edit_original_response(content="Embed sent!", view=None)
            self.stop()
        except discord.Forbidden:
            await interaction.edit_original_response(content="I don't have permission to send messages in this channel.", view=None)
        except discord.HTTPException as e:
            log.error(f"Failed to send embed: {e}")
            await interaction.edit_original_response(content="An error occurred while sending the embed.", view=None)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger, row=1)
    async def cancel_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Embed creation cancelled.", view=None)
        self.stop()


def get_auto_server_setup_embed_view():
     embed = CustomEmbed(
        title="Auto Server Setup",
        description="Choose an option to automatically configure parts of your server.",
        fields=[
            ("🚧", "**Channels**: Create standard channels (e.g., general, rules, announcements).", False),
            ("----------------------------------------------------------------", "", False),
            ("🚧", "**Roles**: Create basic roles (e.g., Member, Moderator, Admin).", False),
            ("----------------------------------------------------------------", "", False),
        ]
    )
     return embed, None

def get_server_verification_embed():
    return CustomEmbed(
        title="Server Verification",
        description="Hey, you can verify yourself here.",
        fields=[("To verify:", "Use the `/verify` command.", False)]
    )