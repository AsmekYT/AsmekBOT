import discord
import embed as em
from functions import database as db
import random
import logging
import datetime

log = logging.getLogger(__name__)

class LoanActionView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx

    @discord.ui.button(label="1. Take a loan", style=discord.ButtonStyle.primary, custom_id="loan_take")
    async def take_loan_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            log.info(f"[take_loan_button] Corrected - Interaction type: {type(interaction)}, Button type: {type(button)}")
            await interaction.response.send_message("Taking a loan is not yet implemented.", ephemeral=True)
        except Exception as e:
            log.error(f"Error in take_loan_button: {e}", exc_info=True)
            try:
                 await interaction.followup.send("Error processing loan request [1].", ephemeral=True)
            except Exception as followup_e:
                 log.error(f"Failed to send fallback message for take_loan_button: {followup_e}")

    @discord.ui.button(label="2. Check unpaid loans", style=discord.ButtonStyle.secondary, custom_id="loan_check_unpaid")
    async def check_unpaid_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            log.info(f"[check_unpaid_button] Corrected - Interaction type: {type(interaction)}, Button type: {type(button)}")
            await interaction.response.send_message("Checking unpaid loans is not yet implemented.", ephemeral=True)
            log.info(f"[check_unpaid_button] Response sent successfully.")
        except Exception as e:
             log.error(f"Error in check_unpaid_button: {e}", exc_info=True)
             try:
                  await interaction.followup.send("Error processing loan request [2].", ephemeral=True)
             except Exception as followup_e:
                  log.error(f"Failed to send fallback message for check_unpaid_button: {followup_e}")


    @discord.ui.button(label="3. Check creditworthiness", style=discord.ButtonStyle.secondary, custom_id="loan_check_credit")
    async def check_credit_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            log.info(f"[check_credit_button] Corrected - Interaction type: {type(interaction)}, Button type: {type(button)}")
            await interaction.response.send_message("Checking creditworthiness is not yet implemented.", ephemeral=True)
        except Exception as e:
            log.error(f"Error in check_credit_button: {e}", exc_info=True)
            try:
                 await interaction.followup.send("Error processing loan request [3].", ephemeral=True)
            except Exception as followup_e:
                 log.error(f"Failed to send fallback message for check_credit_button: {followup_e}")

    @discord.ui.button(label="4. Loan History", style=discord.ButtonStyle.secondary, custom_id="loan_check_archive")
    async def check_archive_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            log.info(f"[check_archive_button] Corrected - Interaction type: {type(interaction)}, Button type: {type(button)}")
            await interaction.response.send_message("Checking loan history is not yet implemented.", ephemeral=True)
        except Exception as e:
            log.error(f"Error in check_archive_button: {e}", exc_info=True)
            try:
                 await interaction.followup.send("Error processing loan request [4].", ephemeral=True)
            except Exception as followup_e:
                 log.error(f"Failed to send fallback message for check_archive_button: {followup_e}")

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            try:
                await interaction.response.send_message("You cannot use this menu.", ephemeral=True)
            except Exception as e:
                 log.error(f"Error in interaction_check: {e}", exc_info=True)
            return False
        return True

async def work(ctx: discord.ApplicationContext):
    user_id = ctx.author.id
    now = datetime.datetime.now(datetime.timezone.utc)

    query_select = 'SELECT work_last_used FROM economy WHERE user_id = %s'
    result = await db.fetchone(query_select, (user_id,))

    last_used = None
    if result and result[0]:
        if isinstance(result[0], datetime.datetime):
             last_used = result[0].replace(tzinfo=datetime.timezone.utc)

    cooldown_duration = datetime.timedelta(hours=1)

    if last_used and (now - last_used < cooldown_duration):
        time_left = cooldown_duration - (now - last_used)
        time_left_formatted = discord.utils.format_dt(now + time_left, style='R')

        embed = em.CustomEmbed(
            title="Cooldown",
            description=f"You can work again {time_left_formatted}.",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed, ephemeral=True)
        return

    earnings = random.randint(10, 50)

    query_update = '''
        INSERT INTO economy (user_id, wallet_coins, work_last_used)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            wallet_coins = wallet_coins + %s,
            work_last_used = %s
    '''
    success = await db.execute(query_update, (user_id, earnings, now, earnings, now))

    if success:
        embed = em.CustomEmbed(
            title='Work Complete!',
            description=f'You worked hard and earned **{earnings}** coins! 💰',
            color=discord.Color.green(),
        )
        await ctx.respond(embed=embed)
    else:
        log.error(f"Failed to update economy data for user {user_id} after work.")
        embed = em.CustomEmbed(
            title='Error',
            description='Failed to record your work. Please try again later or contact an administrator.',
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)


async def balance(ctx: discord.ApplicationContext):
    user_id = ctx.author.id

    query = 'SELECT wallet_coins, bank_coins FROM economy WHERE user_id = %s'
    result = await db.fetchone(query, (user_id,))

    wallet_balance = 0
    bank_balance = 0
    if result:
        wallet_balance = result[0] if result[0] is not None else 0
        bank_balance = result[1] if result[1] is not None else 0

    embed = em.CustomEmbed(
        title=f"{ctx.author.display_name}'s Balance",
        description='',
        color=discord.Color.gold(),
        fields=[
            ('Wallet 👛', f'{wallet_balance} coins', True),
            ('Bank 🏦', f'{bank_balance} coins', True)
        ]
    )
    embed.set_footer(text=f"Total: {wallet_balance + bank_balance} coins | AsmekBOT 2024©")
    await ctx.respond(embed=embed)

async def loan(ctx: discord.ApplicationContext):
    embed = em.CustomEmbed(
        title='Bank Loan Menu',
        description='Select an option below:',
        color=discord.Color.blue(),
        fields=[
            ('1. Take a loan', "Borrow money for a set period (interest applies).", False),
            ('2. Check unpaid loans', "View outstanding loans and payment details.", False),
            ('3. Check creditworthiness', "See the maximum amount you can borrow.", False),
            ('4. Loan History', "View your past paid-off loans.", False)
        ]
    )

    view = LoanActionView(ctx)
    await ctx.respond(embed=embed, view=view, ephemeral=True)