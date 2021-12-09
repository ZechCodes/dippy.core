from dippy.core.api.client import DiscordRestClient
from dippy.core.api.endpoints.channels import CreateMessageRequest
from dippy.core.snowflake import Snowflake
from pytest import fixture, mark
from os import getenv
from time import time


@fixture
def channel_id():
    return Snowflake(getenv("CHANNEL_ID", 0))


@fixture
def user_id():
    return Snowflake(getenv("USER_ID", 0))


@mark.asyncio
@fixture
async def connection():
    return DiscordRestClient(getenv("DISCORD_TOKEN", ""))


@mark.asyncio
async def test_rest_client(channel_id, connection):
    async with connection as client:
        content = f"This is a test {time()}"
        resp = await client.request(CreateMessageRequest(channel_id, content=content))
        assert resp.content == content
