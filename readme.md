# Dippy.Core

This is a bare-bones Discord gateway client that can be used to build Python bot frameworks for Discord. 

## Installation
```shell
pip install dippy.core
```

## Usage

### Connecting
```python
from dippy.core import GatewayConnection, Intents
from asyncio import get_event_loop

client = GatewayConnection("YOUR.TOKEN.HERE", intents=Intents.DEFAULT | Intents.MEMBERS)

loop = get_event_loop()
loop.create_task(client.connect())
loop.run_forever()
```

### Watching For Events
```python
async def on_ready(event_payload):
    print(event_payload.data)

client.on(on_ready, "READY")
```

## Future

- Add models to wrap the event payload data
- Add a caching interface
- Add rate limiting
- Add methods to models for using the gateway
