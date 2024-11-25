import hikari
import lightbulb
import datetime
from config import *

eventutils_plugin = lightbulb.Plugin("Eventutils", default_enabled_guilds=DEFAULT_GUILD)


@eventutils_plugin.command
@lightbulb.command('adventskalender', 'Alle Adventskalender commands')
@lightbulb.app_command_permissions(dm_enabled=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def adventskalender(_: lightbulb.SlashContext):
    pass


# noinspection PyArgumentList
@adventskalender.child
@lightbulb.command(name='info', description='Gibt dir alle nötigen Infos zum Event')
@lightbulb.implements(lightbulb.SlashCommand)
async def info(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Tommys abgefahrener Adventskalender",
        color='#ba070d',
        description=EVENT_DESCR
    )
    await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(eventutils_plugin)
