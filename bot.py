from typing import Optional
from config import *
import hikari
import lightbulb
from hikari import Intents



bot = lightbulb.BotApp(
    TOKEN,
    intents=Intents.ALL,
    banner=None
)


@bot.command
@lightbulb.command("ping", description="The bot's ping.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency * 1000:.2f}ms.")


if __name__ == "__main__":
    bot.run()