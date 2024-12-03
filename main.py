from typing import Optional
from config import *
import hikari
import lightbulb
from hikari import Intents
import aiohttp
import miru
import storageutils.storage
import datetime
import asyncio
import time
import threading
import random

bot = lightbulb.BotApp(
    TOKEN,
    intents=Intents.ALL,
    banner=None
)
client = miru.Client(bot)
bot.load_extensions_from('./extensions/')





def schedule_function(function: any, hour: int, minute: int):
    while True:
        now = datetime.datetime.now()
        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        delay = (target_time - now).total_seconds()
        if delay > 0:
            time.sleep(delay)
            function(bot)
        else:
            next_day = now + datetime.timedelta(days=1)
            target_time = next_day.replace(hour=hour, minute=minute, second=0, microsecond=0)
            delay = (target_time - now).total_seconds()
            time.sleep(delay)
            function()


async def spawn_türchen() -> None:
    view = BasicView
    embed = hikari.Embed(title='EIN TÜRCHEN IST GESPAWNED', description='Sei schnell und drück den Knopf,'
                                                                        'um es zu öffnen.', color=0x00FFFF)
    await bot.rest.create_message(channel=COMMUNITY_CHAT, content=embed, components=view.build())
    client.start_view(view)


@bot.listen()
async def on_starting(_: hikari.StartingEvent) -> None:
    bot.d.client_session = aiohttp.ClientSession()


@bot.listen()
async def on_stopping(_: hikari.StoppingEvent) -> None:
    await bot.d.client_session.close()



if __name__ == "__main__":
    bot.run()
    thread = threading.Thread(target=schedule_function,
                              args=(spawn_türchen, random.randint(11, 24), random.randint(0, 60)))
    thread.daemon = True  # Set the thread as a daemon thread to exit when the main program ends
    thread.start()