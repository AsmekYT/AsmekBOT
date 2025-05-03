import embed as em
import psutil
import discord
import asyncio
import logging

log = logging.getLogger(__name__)

async def ping(ctx: discord.ApplicationContext, bot: discord.Bot):
    loop = asyncio.get_event_loop()
    try:
        cpu_percent = await loop.run_in_executor(None, psutil.cpu_percent, None)
        vm = await loop.run_in_executor(None, psutil.virtual_memory)
        ram_percent = vm.percent
    except Exception as e:
        log.error(f"Failed to get system stats: {e}")
        cpu_percent = "N/A"
        ram_percent = "N/A"


    latency_ms = round(bot.latency * 1000)

    embed = em.CustomEmbed(
        title="Pong! 🏓",
        description="Bot performance and system status:",
        color=discord.Color.blurple(),
        fields=[
            ("Bot Latency:", f"{latency_ms}ms", True),
            ("CPU Usage:", f"{cpu_percent}%", True),
            ("RAM Usage:", f"{ram_percent}%", True),
        ]
    )
    await ctx.respond(embed=embed)


async def version(ctx: discord.ApplicationContext, bot_version: str):
    embed = em.CustomEmbed(
        title="Bot Version",
        description=f"Currently running version: **{bot_version}**",
        color=discord.Color.teal()
    )
    await ctx.respond(embed=embed)