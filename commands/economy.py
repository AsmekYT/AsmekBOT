import mysql
import mysql.connector
import datetime
import embed as em
from functions import database as db
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

        cursor.execute('INSERT INTO wallet (user_id, coins) VALUES (%s, %s) ON DUPLICATE KEY UPDATE coins = coins + %s',
                       (user_id, earnings, earnings))

        cursor.execute('INSERT INTO cooldowns (user_id, last_used) VALUES (%s, %s) ON DUPLICATE KEY UPDATE last_used = %s',
                       (user_id, datetime.datetime.now(), datetime.datetime.now()))

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