# Dippy.Core

This is a bare-bones Discord gateway client that can be used to build Python bot frameworks for Discord. 

## Installation
```shell
pip install dippy.core
```

## Usage

`dippy.core` relies heavily on the [Bevy Package](https://pypi.org/project/bevy/). Since this is not intended as a consumer facing package it will be necessary to directly set up a Bevy context with all of the `dippy.core` dependencies.

### Connecting
```python
import asyncio
from bevy import Context
from asyncio import get_event_loop
from dippy.core import CacheManager, EventDispatch, Intents
from dippy.core.api.api import DiscordAPI
import logging
import os


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


loop = get_event_loop()
loop.run_until_complete(start(loop))
```

## Future

- Add models to wrap the event payload data
- Add rate limiting
- Add methods to models for using the API
