import embed as em
import psutil



class main():
    async def ping(ctx, bot):
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        latency_ms = round(bot.latency * 1000, 1)
        embed = em.CustomEmbed(
            title="Pong!",
            description="Here you can see basic parameters like ping or percent of used CPU.",
            fields=[
                ("-----------------------------------------------------", "", False),
                ("Ping:", f"{latency_ms}ms", True),
                ("-----------------------------------------------------", "", False),
                ("Percent of used CPU:", f"{cpu}%", False),
                ("-----------------------------------------------------", "", False),
                ("Percent of used RAM", f"{ram}%", False),
                ("-----------------------------------------------------", "", False),
            ]
        )
        await ctx.respond(embed=embed)

    async def version(ctx, bot_version):
        embed = em.CustomEmbed(
            title="Code version",
            description="",
            fields=[
                ("-----------------------------------------------------", "", False),
                ("Bot version:", f"{bot_version}", True),
                ("-----------------------------------------------------", "", False),
            ]
        )
        await ctx.respond(embed=embed)


