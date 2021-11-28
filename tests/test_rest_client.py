from bevy import Context
from dippy.core.api.client import DiscordRestClient
from dippy.core.api.endpoints.audit_logs import GetAuditLogRequest
from dippy.core.api.endpoints.guilds import GetGuild, GetGuildMember
from dippy.core.api.endpoints.users import GetUser
from dippy.core.cache.manager import CacheManager
from dippy.core.api.models.guilds import Member
from dippy.core.api.models.users import User
from dippy.core.snowflake import Snowflake
from dippy.core.api.request import (
    RequestModel,
    JSONArgField,
    QueryArgField,
    URLArgField,
)
from pytest import mark
from os import getenv


def test_request_models():
    class TestModel(RequestModel):
        uarg_a: str = URLArgField()
        uarg_b: str = URLArgField()
        uarg_c: str = URLArgField()

        jarg_a: int = JSONArgField()
        jarg_b: int = JSONArgField()
        jarg_c: int = JSONArgField()

        qarg_a: str = QueryArgField()
        qarg_b: str = QueryArgField()
        qarg_c: str = QueryArgField()

    m = TestModel(
        "a", "b", "c", jarg_a=1, jarg_b=2, jarg_c=3, qarg_a="z", qarg_b="y", qarg_c="x"
    )
    assert m.url_args == {"uarg_a": "a", "uarg_b": "b", "uarg_c": "c"}
    assert m.json_args == {"jarg_a": 1, "jarg_b": 2, "jarg_c": 3}
    assert m.query_args == {"qarg_a": "z", "qarg_b": "y", "qarg_c": "x"}


@mark.asyncio
async def test_rest_client():
    async with DiscordRestClient(getenv("DISCORD_TOKEN", "")) as client:
        resp = await client.request(
            GetAuditLogRequest(Snowflake(getenv("GUILD_ID", 0)), limit=1)
        )
        assert len(resp["audit_log_entries"]) == 1


@mark.asyncio
async def test_get_user():
    async with DiscordRestClient(getenv("DISCORD_TOKEN", "")) as client:
        resp = await client.request(GetUser(int(getenv("USER_ID"))))
        assert isinstance(resp, User)


@mark.asyncio
async def test_member_cached():
    context = Context()
    async with context.build(DiscordRestClient, getenv("DISCORD_TOKEN", "")) as client:
        resp = await client.request(
            GetGuildMember(
                Snowflake(getenv("GUILD_ID", 0)), Snowflake(getenv("USER_ID", 0))
            )
        )
        member = context.get(CacheManager).get(
            Member, getenv("GUILD_ID", 0), getenv("USER_ID", 0)
        )
        assert resp._data is member._data


@mark.asyncio
async def test_user_cached():
    context = Context()
    async with context.build(DiscordRestClient, getenv("DISCORD_TOKEN", "")) as client:
        member = await client.request(
            GetGuildMember(
                Snowflake(getenv("GUILD_ID", 0)), Snowflake(getenv("USER_ID", 0))
            )
        )
        user = await client.request(GetUser(Snowflake(getenv("USER_ID", 0))))
        assert user._data is member.user._data


@mark.asyncio
async def test_get_guild():
    context = Context()
    async with context.build(DiscordRestClient, getenv("DISCORD_TOKEN", "")) as client:
        guild = await client.request(GetGuild(Snowflake(getenv("GUILD_ID", 0))))

        assert guild.id == Snowflake(getenv("GUILD_ID", 0))
        str(guild)
