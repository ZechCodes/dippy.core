from dippy.core.api.client import DiscordRestClient
from dippy.core.api.endpoints.stage import *
from dippy.core.snowflake import Snowflake
from pytest import mark
from os import getenv
from dotenv import load_dotenv

load_dotenv()


@mark.asyncio
async def test_stage():
    async with DiscordRestClient(getenv("DISCORD_TOKEN", "")) as client:
        resp = await client.request(
            CreateStageInstance(
                channel_id=Snowflake(getenv("CHANNEL_ID")),
                topic=Snowflake(getenv("TOPIC")),
            )
        )


@mark.asyncio
async def test_get_stage():
    async with DiscordRestClient(getenv("DISCORD_TOKEN", "")) as client:
        resp = await client.request(GetStageInstance(Snowflake(getenv("CHANNEL_ID"))))


@mark.asyncio
async def test_modify_stage_instance():
    async with DiscordRestClient(getenv("DISCORD_TOKEN", "")) as client:
        resp = await client.request(
            ModifyStageInstance(
                Snowflake(getenv("CHANNEL_ID")), topic=Snowflake(getenv("TOPIC"))
            )
        )


@mark.asyncio
async def delete_stage_instance():
    async with DiscordRestClient(getenv("DISCORD_TOKEN", "")) as client:
        resp = await client.request(
            DeleteStageInstance(Snowflake(getenv("CHANNEL_ID")))
        )
