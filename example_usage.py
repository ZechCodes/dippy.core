"""This is a barebones interface to the Discord Gateway and API.

# ☢️ THIS IS ALPHA SOFTWARE AND WILL BE BUGGY ☢️

## Currently Supported
- API wrapper that has some endpoints implemented
- Caching (as Discord expects you to do)

## Currently not supported
- Gateway client
- Most API endpoints

## Usage
Currently only the API wrapper is functional. To use just create an instance of dippy.core.api.client.DiscordRestClient.
You can then request endpoints by creating an instance of the desired endpoint request model and passing that to the
client instance's request method."""

import asyncio
from dippy.core.api.client import DiscordRestClient
from dippy.core.api.endpoints.users import GetUser
from os import getenv


async def start():
    async with DiscordRestClient(getenv("DISCORD_TOKEN", "")) as client:
        user_id = int(input("What is your Discord user ID? "))
        resp = await client.request(GetUser(user_id))
        print(f"Hello {resp.username}!!!")


def main():
    asyncio.run(start())


if __name__ == "__main__":
    main()
