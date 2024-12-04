import hikari
import lightbulb
import storageutils.storage
from config import *
import miru
from typing import Optional

from embed_gen import GET_TUERCHEN_COMMAND
from storageutils.storage import get_user_tuerchen

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
    await ctx.respond('Oh oh, dieser Command wurde leider noch nicht implementiert :(', flags=hikari.MessageFlag.EPHEMERAL)


@eventutils_plugin.command
@lightbulb.option('member', 'Das hier ist eine noch bessere Beschreibung', type=hikari.Member)
@lightbulb.option('anzahl', 'Das hier ist eine tolle Beschreibung', type=int)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('türchen_abziehen', 'Zieht dem Member die spezifizierte Anzahl an Türchen ab.',)
@lightbulb.implements(lightbulb.SlashCommand)
async def tuerchen_abziehen(ctx: lightbulb.Context) -> None:
    await ctx.respond(f'{ctx.options["member"]} wurden {ctx.options["anzahl"]} Türchen abgezogen.', flags=hikari.MessageFlag.EPHEMERAL)
    await storageutils.storage.subtract_türchen(ctx.options['member'], ctx.options['anzahl'])


@eventutils_plugin.command
@lightbulb.option('member', 'Das hier ist eine noch bessere Beschreibung', type=hikari.Member)
@lightbulb.option('anzahl', 'Das hier ist eine tolle Beschreibung', type=int)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('türchen_geben', 'Gibt dem Member die spezifizierte Anzahl an Türchen')
@lightbulb.implements(lightbulb.SlashCommand)
async def tuerchen_abziehen(ctx: lightbulb.Context) -> None:
    await ctx.respond(f'{ctx.options["member"]} wurden {ctx.options["anzahl"]} Türchen gegeben.', flags=hikari.MessageFlag.EPHEMERAL)
    await storageutils.storage.add_türchen(ctx.options['member'], ctx.options['anzahl'])


@eventutils_plugin.command
@lightbulb.option('member', 'Lass diesen Parameter weg, wenn du deine eigenen Türchen abfragen willst.', type=hikari.Member, required=False)
@lightbulb.command('türchen', 'Zeigt dir die Anzahl an Türchen von dir oder anderen an.')
@lightbulb.implements(lightbulb.SlashCommand)
async def tuerchen(ctx: lightbulb.Context) -> None:
    if ctx.options["member"] is None:
        await ctx.respond(await GET_TUERCHEN_COMMAND(ctx.member, await get_user_tuerchen(ctx.member)), flags=hikari.MessageFlag.EPHEMERAL)

    else:
        await ctx.respond(
            await GET_TUERCHEN_COMMAND(ctx.options["member"], await get_user_tuerchen(ctx.options["member"])),
            flags=hikari.MessageFlag.EPHEMERAL)



@eventutils_plugin.command
@lightbulb.command('leaderboard', description='Zeigt das Leaderboard')
@lightbulb.implements(lightbulb.SlashCommand)
async def leaderboard(ctx: lightbulb.Context) -> None:
    await ctx.respond(await storageutils.storage.gen_leaderboard(), flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(eventutils_plugin)
