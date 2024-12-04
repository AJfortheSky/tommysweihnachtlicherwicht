from config import *
import hikari
import lightbulb
from hikari import Intents
import aiohttp
import miru
import storageutils.storage
import random
from datetime import datetime
from embed_gen import *
from hikari import Embed


counter: int = 0

bot = lightbulb.BotApp(
    TOKEN,
    intents=Intents.ALL,
    banner=None
)
client = miru.Client(bot)

bot.load_extensions_from('./extensions/')



class BasicView(miru.View):

    @miru.button(label='Drück mich!', style=hikari.ButtonStyle.DANGER)
    async def basic_button(self, ctx: miru.ViewContext, button: miru.Button):
        await storageutils.storage.insert_user(ctx.member, 1)
        await ctx.edit_response(hikari.Embed(title="Türchen Offen!", description='Da war wohl jemand schneller...',
                                             color='#e61405'))
        button.label = 'Disabled'
        self.stop()


@bot.listen(hikari.GuildMessageCreateEvent)
async def count_msgs(event: hikari.GuildMessageCreateEvent):
    threshold: int = random.randint(15, 70)
    global counter
    if not event.author.is_bot and event.channel_id in ALLOWED_CHANNELS:
        counter += 1
        print(f'Es wurden {counter} Nachrichten geschickt.')

    if counter == threshold:
        print()
        await spawn_türchen(event)
        counter = 0


async def spawn_türchen(event: hikari.GuildMessageCreateEvent) -> None:
    view = BasicView()
    embed = TUERCHEN_SPAWN_EMBED
    await event.message.respond(embed, components=view)
    print('ich wurde gecalled')
    client.start_view(view)


@bot.listen()
async def on_starting(_: hikari.StartingEvent) -> None:
    bot.d.client_session = aiohttp.ClientSession()


@bot.listen()
async def on_stopping(_: hikari.StoppingEvent) -> None:
    await bot.d.client_session.close()


if __name__ == "__main__":
    bot.run()

