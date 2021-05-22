"""This is a very barebones interface to the Discord Gateway and API.

# ☢️ THIS IS ALPHA SOFTWARE AND WILL BE BUGGY ☢️

## Currently Supported
- Gateway events
- API wrapper to send messages
- Simple embed API for use with the send messages endpoint
- Caching (as Discord expects you to do)
- Intents

## Currently not supported
- Gateway sharding
- API wrappers for everything but the message send endpoint

## Usage
This is built using the Bevy package for dependency injection. This allows for simple swapping out of components but
since this is a bare bones implementation it is incumbent on you to supply the appropriate components through Bevy.

### Necessary Components
- API: `dippy.core.api.api.DiscordAPI` is the builtin implementation
- Async Loop: `asyncio.get_event_loop()` is all that's necessary
- Event Dispatch `dippy.core.EventDispatch` is the builtin implementation that uses the Gully package's streams
- Cache: `dippy.core.CacheManager` is the builtin implementation that will cache users, guilds, channels, members, and
messages.

To set it up and connect you will need to create a `bevy.Context` instance. Add the async loop to that context. Next
use the context's `create` method to make an instance of the API class, passing it the discord token and the intents
that you would want to use. `dippy.core.Intents.ALL` will enable all intents, `dippy.core.Intents.DEFAULT` will enable
all intents except messages and presences, and using the pipe operator it is possible to enable a selection of intents
`dippy.core.Intents.MESSAGES | dippy.core.Intents.PRESENCES` will enable just messages and presences. You'll want to do
this as an `async with` so that the dippy.core API can ensure everything closes correctly in the case of a crash.

Once that's done add the api instance to the context as it is the client object and will be useful to have. Next create
and add the event dispatch, then the cache.

At this point it's ready to be connected. Event handlers can be registered using `events.on(event_name, event_handler)`.
The `READY` event will be triggered when the Discord gateway is ready which will actually be before the gateway has sent
any guilds or members to cache. So it's best to sleep for 2 seconds before doing anything from the `READY` event.

Once all the event handlers are in place the bot can be connected with `await api.connect()`. This will run until it
either crashes or the process is stopped.
"""

import asyncio
from bevy import Context
from asyncio import get_event_loop
from dippy.core import CacheManager, EventDispatch, Intents
from dippy.core.api.api import DiscordAPI
import logging
import os


logging.basicConfig(level=logging.INFO)
logging.getLogger("Heartbeat").setLevel(logging.DEBUG)


async def start(loop):
    context = Context()
    context.add(loop)

    async with context.create(
        DiscordAPI, os.getenv("DISCORD_TOKEN"), intents=Intents.ALL
    ) as api:
        context.add(api)

        events = context.create(EventDispatch)
        context.add(events)

        cache = context.create(CacheManager)
        context.add(cache)

        async def ready(event):
            await asyncio.sleep(2)
            logging.info(f"Everything should be ready now {event.user.username}!")

        events.on("READY", ready)

        await api.connect()


def main():
    loop = get_event_loop()
    loop.run_until_complete(start(loop))


if __name__ == "__main__":
    main()
