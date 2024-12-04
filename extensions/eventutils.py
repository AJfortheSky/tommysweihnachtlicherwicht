import hikari
import lightbulb
import storageutils.storage
from config import *
import miru

client = miru.Client(lightbulb.BotApp(TOKEN, ignore_bots=True, owner_ids=[BOT_OWNER]))

eventutils_plugin = lightbulb.Plugin("Eventutils", default_enabled_guilds=DEFAULT_GUILD)


class BasicView(miru.View):

    @miru.button(label='Drück mich!', style=hikari.ButtonStyle.DANGER)
    async def basic_button(self, ctx: miru.ViewContext, button: miru.Button):
        await storageutils.storage.insert_user(ctx.member, 1)
        await ctx.edit_response('You have been added to the database')
        self.stop()


# noinspection PyArgumentList
@eventutils_plugin.command
@lightbulb.command(name='info', description='Gibt dir alle nötigen Infos zum Event')
@lightbulb.implements(lightbulb.SlashCommand)
async def info(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Tommys abgefahrener Adventskalender",
        color='#ba070d',
        description=EVENT_DESCR
    )

    await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)


@eventutils_plugin.command
@lightbulb.option('member', 'Das hier ist eine noch bessere Beschreibung', type=hikari.Member)
@lightbulb.option('anzahl', 'Das hier ist eine tolle Beschreibung', type=int)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('türchen_abziehen', 'Zieht dem Member die spezifizierte Anzahl an Türchen ab.',)
@lightbulb.implements(lightbulb.SlashCommand)
async def tuerchen_abziehen(ctx: lightbulb.Context) -> None:
    await ctx.respond(f'{ctx.options['member']} wurden {ctx.options['anzahl']} abgezogen.', flags=hikari.MessageFlag.EPHEMERAL)
    await storageutils.storage.subtract_türchen(ctx.options['member'], ctx.options['anzahl'])


@eventutils_plugin.command
@lightbulb.option('member', 'Das hier ist eine noch bessere Beschreibung', type=hikari.Member)
@lightbulb.option('anzahl', 'Das hier ist eine tolle Beschreibung', type=int)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('türchen_geben', 'Gibt dem Member die spezifizierte Anzahl an Türchen')
@lightbulb.implements(lightbulb.SlashCommand)
async def tuerchen_abziehen(ctx: lightbulb.Context) -> None:
    await ctx.respond(f'{ctx.options['member']} wurden {ctx.options['anzahl']} abgezogen.', flags=hikari.MessageFlag.EPHEMERAL)
    await storageutils.storage.subtract_türchen(ctx.options['member'], ctx.options['anzahl'])


@eventutils_plugin.command
@lightbulb.command('leaderboard', description='Zeigt das Leaderboard')
@lightbulb.implements(lightbulb.SlashCommand)
async def leaderboard(ctx: lightbulb.Context) -> None:
    await ctx.respond(await storageutils.storage.gen_leaderboard(), flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(eventutils_plugin)
