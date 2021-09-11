from dippy.core.api.client import DiscordRestClient
from dippy.core.api.endpoints.invite import GetInvite, DeleteInvite
from dippy.core.snowflake import Snowflake
from pytest import mark
from os import getenv
from dotenv import load_dotenv

load_dotenv()


@mark.asyncio
async def test_get_invite():
    async with DiscordRestClient(getenv("DISCORD_TOKEN", "")) as client:
        resp = await client.request(GetInvite(Snowflake(getenv("INVITE_CODE", ""))))
        assert resp.get("code")


@mark.asyncio
async def test_delete_invite():
    async with DiscordRestClient(getenv("DISCORD_TOKEN", "")) as client:
        resp = await client.request(DeleteInvite(Snowflake(getenv("INVITE_CODE", ""))))
        assert resp.get("code")
