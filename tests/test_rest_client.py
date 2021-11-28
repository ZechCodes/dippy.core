from bevy import Context
from dippy.core.api.client import DiscordRestClient
from dippy.core.api.endpoints.audit_logs import GetAuditLogRequest
from dippy.core.api.endpoints.guilds import GetGuild, GetGuildMember
from dippy.core.api.endpoints.users import GetUser
from dippy.core.api.models.guilds import Member
from dippy.core.api.models.users import User
from dippy.core.snowflake import Snowflake
from dippy.core.api.request import (
    RequestModel,
    JSONArgField,
    QueryArgField,
    URLArgField,
)
from pytest import fixture, mark, xfail
from os import getenv


@fixture
def channel_id():
    return Snowflake(getenv("CHANNEL_ID", 0))


@fixture
def guild_id():
    return Snowflake(getenv("GUILD_ID", 0))


@fixture
def user_id():
    return Snowflake(getenv("USER_ID", 0))


@mark.asyncio
@fixture
async def connection():
    return DiscordRestClient(getenv("DISCORD_TOKEN", ""))


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
async def test_rest_client(guild_id, connection):
    async with connection as client:
        resp = await client.request(GetAuditLogRequest(guild_id, limit=1))
        assert len(resp["audit_log_entries"]) == 1


@mark.asyncio
async def test_get_user(user_id, connection):
    async with connection as client:
        resp = await client.request(GetUser(user_id))
        assert isinstance(resp, User)


@mark.asyncio
async def test_member_cached(user_id, guild_id, connection):
    async with connection as client:
        resp = await client.request(GetGuildMember(guild_id, user_id))
        member = client.cache.get(Member, guild_id, user_id)
        assert resp._state is member._state


@mark.asyncio
@mark.skip("Currently don't want to dedicate time to perfecting the caching")
async def test_user_cached(user_id, guild_id, connection):
    async with connection as client:
        member = await client.request(GetGuildMember(guild_id, user_id))
        user = await client.request(GetUser(user_id))
        xfail(
            "Requests that return fields that are also cacheable models don't update the cache with the value of the"
            "fields"
        )
        assert user._state is member.user._state


@mark.asyncio
async def test_get_guild(guild_id, connection):
    async with connection as client:
        guild = await client.request(GetGuild(guild_id))

        assert guild.id == guild_id
