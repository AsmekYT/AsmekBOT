import aiohttp
import mysql
import mysql.connector
import datetime
import discord
import embed as em
from functions import database as db
import modal as md
import random



class main():
    async def work(ctx):
        user_id = ctx.author.id
        conn = mysql.connector.connect(**db.mysql_config)
        cursor = conn.cursor()

        cursor.execute('SELECT last_used FROM cooldowns WHERE user_id = %s', (user_id,))
        result = cursor.fetchone()

        if result is not None:
            last_used = result[0]
            now = datetime.datetime.now()
            cooldown_duration = datetime.timedelta(days=1)
            if now - last_used < cooldown_duration:
                time_left = cooldown_duration - (now - last_used)
                seconds_left = round(time_left.total_seconds())

                hours = seconds_left // 3600
                minutes = (seconds_left % 3600) // 60
                seconds = seconds_left % 60
                time_left_formatted = f'{hours} hours {minutes:02} minutes and {seconds:02} seconds'

                embed = em.CustomEmbed(
                    title="Cooldown",
                    description="You are on cooldown.",
                    fields=[("Time left:", time_left_formatted, False)]
                )
                await ctx.respond(embed=embed, ephemeral=True)
                conn.close()
                return

        earnings = random.randint(1, 100)

        cursor.execute(
            'INSERT INTO user_data (user_id, wallet_coins, work_last_used) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE wallet_coins = wallet_coins + %s, work_last_used = %s',
            (user_id, earnings, datetime.datetime.now(), earnings, datetime.datetime.now()))

        conn.commit()
        conn.close()

        embed = em.CustomEmbed(
            title='Work',
            description='',
            fields=[('You worked hard and earned:', f'{earnings} coins!', False)]
        )
        await ctx.respond(embed=embed)



    async def balance(ctx):
        user_id = ctx.author.id
        conn = mysql.connector.connect(**db.mysql_config)
        cursor = conn.cursor()

        cursor.execute('SELECT coins FROM wallet WHERE user_id = %s', (user_id,))
        result = cursor.fetchone()

        if result is None:
            balance = 0
        else:
            balance = result[0]

        conn.close()

        embed = em.CustomEmbed(
            title='Balance',
            description='',
            fields=[('Your current balance:', f'{balance} coins', False)]
        )
        await ctx.respond(embed=embed)


    async def loan(ctx):
        user_id = ctx.author.id

        loan_amount = 0
        duration = 0
        interest = 0

        def change_loan_duration(interaction):
            pass


        async def change_loan_amount(interaction):
            #brain rot moment 2
            new_amount = md.AmountModal()

            await new_amount.callback(interaction)


        async def take_loan(interaction):

            embed2 = em.CustomEmbed(
                title='Take a Loan',
                description='In this menu you can take a loan',
                fields=[
                    ('How much money do you want to loan:', loan_amount, False),
                    ('Duration of the loan:', duration, False),
                    ('Loan interest rate:', interest, False),
                ]
            )

            # Brain rot moment
            view2 = em.UniversalButtonView(label="Change loan amount", style=discord.ButtonStyle.primary,
                                           callback=change_loan_amount)
            await interaction.respond(embed=embed2, view=view2, ephemeral=True)

        embed = em.CustomEmbed(
            title='Bank Loan',
            description='Select option you are interested in.',
            fields=[
                ('1. Take a loan:', "By selecting this option, you can take a loan for some period of time", False),
                ('2. Check unpaid loans', "By selecting this option, you can check if you have unpaid loans and see how muhc do you have to pay", False),
                ('3. Check your creditworthiness', "By selecting this option, you can check how much money you can loan from our bank.", False),
                ('4. Check archive loans', "By selecting this option, you can check loans you have paid off in the past.", False)
            ]
        )

        view = em.UniversalButtonView(label="1. Take a loan", style=discord.ButtonStyle.primary, callback=take_loan)
        await ctx.respond(embed=embed, view=view, ephemeral=True)


